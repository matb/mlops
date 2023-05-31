from typing import NamedTuple

import kfp
from kfp.components import InputPath, OutputPath, create_component_from_func
import pandas as pd


def download_data(url: str, out: OutputPath(str)):
   import pandas as pd
   pd.read_csv(url
               ).to_csv(out, index=False)


def clean_data(data: InputPath(str), out: OutputPath(str)):
    import pandas as pd
    df = pd.read_csv(data)
    df = df.set_index("ID")

    for key in ["INCOME", "HOME_VAL", "OLDCLAIM"]:
        df[key] = df[key].str.replace("$", "", regex=False).str.replace(",", ".").astype(float)
    df = df.drop("BIRTH", axis=1)
    df.to_csv(out)


def create_features(data_dir: InputPath(str), feature_path: OutputPath(str), target_path: OutputPath(str)):
    import pandas as pd

    df = pd.read_csv(data_dir, index_col="ID")
    columns_to_drop = ['OCCUPATION', 'CAR_TYPE', 'KIDSDRIV',
                       'YOJ', 'PARENT1', 'URBANICITY',
                       "TIF", "RED_CAR", "CAR_USE"]
    features = df.drop(columns_to_drop, axis=1).copy()
    target = features.pop("CLAIM_FLAG")

    features.to_csv(feature_path)
    target.to_csv(target_path)


def prepare_numerics(feature_path: InputPath(str), out: OutputPath(str)):
    """
    This function will turn numeric data on an arbitrary scale into a normalized version
    via the function ((X — X min)/ (X max — X min))
    """
    import pandas as pd
    features = pd.read_csv(feature_path, index_col="ID")
    result = features.copy()

    for name, column in features.items():
        if column.dtype == object:
            continue
        max_value = column.max()
        min_value = column.min()
        result[name] = (column - min_value) / (max_value - min_value)
    result.to_csv(out)


def prepare_categorical(feature_path: InputPath(str), out: OutputPath(str)):
    """
    This function is using the pd.get_dummies function to encode the categorical varialbes
    into binary ones s.t. they turn numeric and are usable by our model later.

    e.g.  [["Gender"]:["male"],["female"],["female"]] -> [["is_male", "is_female"]:[1,0],[0,1],[0,1]]
    """
    import pandas as pd
    features = pd.read_csv(feature_path, index_col="ID")
    encoded_features = []
    for key, feature in features.items():
        if feature.dtype != object:
            continue
        encoded = pd.get_dummies(feature, prefix=key, prefix_sep="_")
        encoded_features.append(encoded)
    df = pd.concat(encoded_features, axis=1)
    df.to_csv(out)


def combine_data(
        numeric_features: InputPath(str),
        categoric_features: InputPath(str),
        target: InputPath(),
        out:OutputPath() ):

    import pandas as pd
    dfs = [
        pd.read_csv(numeric_features, index_col="ID"),
        pd.read_csv(categoric_features, index_col="ID"),
        pd.read_csv(target, index_col="ID")
    ]
    preprocessed = pd.concat(dfs, axis=1)
    preprocessed = preprocessed.reset_index()
    preprocessed.to_csv(out)


def train(
        data: InputPath(str),
        model_out: OutputPath(str),
        train_out: OutputPath(str),
        test_out: OutputPath(str)):

    import joblib
    import pandas as pd
    import tensorflow_decision_forests as tfdf

    data = pd.read_csv(data)
    test_df = data.sample(frac=0.1)
    train_df = data.drop(test_df.index)
    train_df.to_csv(train_out, index=False)
    test_df.to_csv(test_out, index=False)

    train_df = train_df.set_index("ID")
    test_df = test_df.set_index("ID")

    # Convert the dataset into a TensorFlow dataset.
    train_ds = tfdf.keras.pd_dataframe_to_tf_dataset(train_df, label="CLAIM_FLAG")

    # Train a Random Forest model.
    model = tfdf.keras.RandomForestModel()
    model.fit(train_ds)
    joblib.dump(model, model_out)


@kfp.dsl.pipeline(
    name="Car-Insurance"
)
def exec_data_transformation_pipeline():
    download_operator = create_component_from_func(
        download_data, packages_to_install=["pandas"]
    )
    clean_op = create_component_from_func(clean_data, packages_to_install=["pandas"])
    seperator_op = create_component_from_func(create_features, packages_to_install=["pandas"])
    prepare_cat_op = create_component_from_func(
        prepare_categorical, packages_to_install=["pandas"]
    )
    prepare_num_op = create_component_from_func(prepare_numerics, packages_to_install=["pandas"])
    combine_op = create_component_from_func(combine_data, packages_to_install=["pandas"])
    train_operator = create_component_from_func(
        train, packages_to_install=["pandas", "tensorflow_decision_forests", "joblib"]
    )

    download = download_operator("https://media.githubusercontent.com/media/mtaschenberger/data/main/car_insurance.csv")
    cleaned = clean_op(download.output)
    separated = seperator_op(cleaned.output)
    features_cat = prepare_cat_op(separated.outputs["feature"])
    features_num = prepare_num_op(separated.outputs["feature"])

    prepared = combine_op(features_num.output, features_cat.output, separated.outputs["target"])
    _ = train_operator(prepared.output)


if __name__ == "__main__":
    # Compiling the pipeline
    kfp.compiler.Compiler().compile(
        exec_data_transformation_pipeline, __file__ + ".yaml"
    )
