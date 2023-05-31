"""
### Task
Now please create one new pipelines with the model we have below.
Split the pipeline into different groups:

   1. the download
   2. training

The exact location is market in the code below

Help: a usefull annotation might be

    def download_data(features: OutputPath(str), target: OutputPath(str)) -> NamedTuple("output",
                                                                                    [("features", str),
                                                                                     ("target", str)]):
"""
from collections import namedtuple
from typing import NamedTuple

import kfp
from kfp.components import InputPath, OutputPath, create_component_from_func


def download_data(features: OutputPath(str), target: OutputPath(str)) -> NamedTuple("output",
                                                                                    [("features", str),
                                                                                     ("target", str)]):
    from collections import namedtuple
    from sklearn import datasets
    import pandas as pd

    iris = datasets.load_iris()
    pd.DataFrame(iris.data).to_csv(features, header=False, index=False)
    pd.DataFrame(iris.target).to_csv(target, header=False, index=False)
    return namedtuple('output', ['features', 'target'])(features, target)


def train(
    features: InputPath(),
    target: InputPath(),
    model_out: OutputPath(),
):
    import json
    import pandas as pd
    import joblib
    from sklearn.model_selection import train_test_split
    import tensorflow as tf

    features = pd.read_csv(features)
    target = pd.read_csv(target)

    features_train, features_test, labels_train, labels_test = train_test_split(
        features.values, target.values, test_size=0.2, random_state=42
    )

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(10, activation='relu', input_shape=(4,)),
        tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(3, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(features_train, labels_train, epochs=100, batch_size=32)

    loss, accuracy = model.evaluate(features_test, labels_test)
    print(f'Test loss: {loss}')
    print(f'Test accuracy: {accuracy}')
    # Step 6: Save the trained model
    model.save(f'models/iris/latest')
    print("Model saved successfully!")
    joblib.dump(model, model_out)
    metrics = {
        "metrics": [
            {
                "name": "accuracy-score",
                "numberValue": accuracy,
                "format": "PERCENTAGE",
            }
        ]
    }
    return [json.dumps(metrics)]


@kfp.dsl.pipeline(
    name="Conditional execution pipeline",
    description="Shows how to use dsl.Condition().",
)
def exec_data_transformation_pipeline():
    download_operator = create_component_from_func(
        download_data, packages_to_install=["scikit-learn", "pandas"]
    )

    train_operator = create_component_from_func(
        train, packages_to_install=["pandas", "scikit-learn", "tensorflow", "joblib"]
    )
    download = download_operator()
    _ = train_operator( download.outputs["features"], download.outputs["target"])



if __name__ == "__main__":
    # Compiling the pipeline
    kfp.compiler.Compiler().compile(
        exec_data_transformation_pipeline, __file__ + ".yaml"
    )

