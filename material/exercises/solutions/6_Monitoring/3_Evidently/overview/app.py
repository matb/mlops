import pprint

import numpy as np
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
from evidently.report import Report
from evidently.test_suite import TestSuite
from evidently.tests import *
from sklearn.datasets import fetch_california_housing


def prepare_data():
    data = fetch_california_housing(as_frame=True)
    housing_data = data.frame
    housing_data.rename(columns={'MedHouseVal': 'target'}, inplace=True)
    housing_data['prediction'] = housing_data['target'].values + np.random.normal(0, 1, housing_data.shape[0])
    reference = housing_data.sample(n=5000, replace=False)
    current = housing_data.sample(n=5000, replace=False)

    return reference, current


def create_datadrift_report(reference, current):
    # Report for a Data Drift
    report = Report(metrics=[
        DataDriftPreset(),
    ])

    report.run(reference_data=reference, current_data=current)
    pprint.pprint(report.as_dict())


def create_target_report(reference, current):
    num_target_drift_report = Report(metrics=[
        TargetDriftPreset(),
    ])
    num_target_drift_report.run(reference_data=reference, current_data=current)
    pprint.pprint(num_target_drift_report.as_dict())


def test_data(reference, current):
    tests = TestSuite(tests=[
        TestNumberOfColumnsWithMissingValues(),
        TestNumberOfRowsWithMissingValues(),
        TestNumberOfConstantColumns(),
        TestNumberOfDuplicatedRows(),
        TestNumberOfDuplicatedColumns(),
        TestColumnsType(),
        TestNumberOfDriftedColumns(),
    ])

    tests.run(reference_data=reference, current_data=current)
    pprint.pprint(tests.as_dict())


def main():
    reference, current = prepare_data()

    create_datadrift_report(reference, current)

    create_target_report(reference, current)

    test_data(reference, current)


if __name__ == '__main__':
    main()
