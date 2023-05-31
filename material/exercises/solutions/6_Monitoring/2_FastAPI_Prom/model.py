import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

SUB_SET = ["age", "workclass", "education", "education_num", "marital_status", "race", "sex", "hours_per_week",
           "income_flag"]
HEADER = ["age", "workclass", "fnlwgt", "education", "education_num", "marital_status", "occupation", "relationship",
          "race", "sex", "capital_gain", "capital_loss", "hours_per_week", "native_country", "income_flag"]


def get_preprocessor():
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    numeric_features = ["age", "education_num", "hours_per_week"]
    categorical_features = ["workclass", "education", "marital_status", "race", "sex"]

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)])

    return preprocessor


def evaluate(model, test_features, test_target):
    predictions = model.predict(test_features)
    score = model.score(test_features, test_target)
    print(f"Model scored: {score}")
    matrix = confusion_matrix(test_target, predictions).tolist()  # .tolist() to convert np array to list.
    return matrix


def clean_data(data):
    for col in data.columns:
        if data[col].dtype == "object":
            data[col] = data[col].str.strip()
    return data


def main():
    df = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data", names=HEADER)
    df = df[SUB_SET]
    df = clean_data(df)
    features = df.copy()
    target = features.pop("income_flag")
    target = target.map({'<=50K': 0, '>50K': 1})
    preprocessor = get_preprocessor()
    estimator = RandomForestClassifier()
    pipe = Pipeline(steps=[('preprocessor', preprocessor),
                           ('classifier', estimator)]
                    )
    train_features, test_features, train_target, test_target = train_test_split(features, target, test_size=0.2)
    pipe.fit(train_features, train_target)
    matrix = evaluate(pipe, test_features, test_target)
    print(f"{matrix}")
    joblib.dump(pipe, "models/model.joblib")


if __name__ == '__main__':
    main()
