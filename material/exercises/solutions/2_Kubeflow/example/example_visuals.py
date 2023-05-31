import os

import kfp
from kfp.components import OutputArtifact, create_component_from_func_v2
from kfp.v2 import dsl
from kfp.v2.dsl import (HTML, ClassificationMetrics, Markdown, Metrics, Output,
                        component)


def digit_classification(metrics: Output[Metrics]):
    from sklearn import datasets, model_selection
    from sklearn.linear_model import LogisticRegression

    iris = datasets.load_iris()

    X = iris.data
    y = iris.target
    test_size = 0.33
    seed = 7

    kfold = model_selection.KFold(n_splits=10, random_state=seed, shuffle=True)
    model = LogisticRegression()
    scoring = "accuracy"
    results = model_selection.cross_val_score(model, X, y, cv=kfold, scoring=scoring)

    X_train, X_test, y_train, y_test = model_selection.train_test_split(
        X, y, test_size=test_size, random_state=seed
    )
    model.fit(X_train, y_train)
    result = model.score(X_test, y_test)
    metrics.log_metric("accuracy", (result * 100.0))


def wine_classification(metrics: Output[ClassificationMetrics]):
    from sklearn.datasets import load_wine
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import roc_curve
    from sklearn.model_selection import cross_val_predict, train_test_split

    X, y = load_wine(return_X_y=True)
    y = y == 1

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    rfc = RandomForestClassifier(n_estimators=10, random_state=42)
    rfc.fit(X_train, y_train)
    y_scores = cross_val_predict(rfc, X_train, y_train, cv=3, method="predict_proba")
    fpr, tpr, thresholds = roc_curve(
        y_true=y_train, y_score=y_scores[:, 1], pos_label=True
    )
    metrics.log_roc_curve(fpr, tpr, thresholds)


def iris_sgdclassifier(test_samples_fraction: float, metrics: Output[ClassificationMetrics]):
    from sklearn import datasets, model_selection
    from sklearn.linear_model import SGDClassifier
    from sklearn.metrics import confusion_matrix

    iris_dataset = datasets.load_iris()
    train_x, test_x, train_y, test_y = model_selection.train_test_split(
        iris_dataset['data'], iris_dataset['target'], test_size=test_samples_fraction)


    classifier = SGDClassifier()
    classifier.fit(train_x, train_y)
    predictions = model_selection.cross_val_predict(classifier, train_x, train_y, cv=3)
    metrics.log_confusion_matrix(
        ['Setosa', 'Versicolour', 'Virginica'],
        confusion_matrix(train_y, predictions).tolist() # .tolist() to convert np array to list.
    )



@component()
def html_visualization(html_artifact: Output[HTML]):
    html_content = "<!DOCTYPE html><html><body><h1>Hello world</h1></body></html>"
    with open(html_artifact.path, "w") as f:
        f.write(html_content)


@component()
def markdown_visualization(markdown_artifact: Output[Markdown]):
    markdown_content = "## Hello world \n\n Markdown content"
    with open(markdown_artifact.path, "w") as f:
        f.write(markdown_content)


@dsl.pipeline(name="metrics-visualization-pipeline")
def metrics_visualization_pipeline():
    wine_classification_op = create_component_from_func_v2(
        wine_classification, packages_to_install=["scikit-learn"]
    )()
    iris_sgdclassifier_op = create_component_from_func_v2(
        iris_sgdclassifier, packages_to_install=["scikit-learn", "joblib"]
    )(test_samples_fraction=0.3)
    digit_classification_op = create_component_from_func_v2(
        digit_classification, packages_to_install=["scikit-learn"]
    )()
    html_visualization_op = html_visualization()
    markdown_visualization_op = markdown_visualization()


if __name__ == "__main__":
    compiler = kfp.compiler.Compiler(mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE)
    compiler.compile(metrics_visualization_pipeline, __file__ + ".yaml")
