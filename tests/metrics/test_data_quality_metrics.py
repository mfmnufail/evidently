import pandas as pd

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.metrics.base_metric import InputData
from evidently.metrics import DataQualityMetrics
from evidently.metrics import DataQualityStabilityMetrics
from evidently.metrics import DataQualityValueListMetrics
from evidently.metrics import DataQualityValueRangeMetrics
from evidently.metrics import DataQualityValueQuantileMetrics
from evidently.metrics import DataQualityCorrelationMetrics


def test_data_quality_metrics() -> None:
    test_dataset = pd.DataFrame({"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 2, 2, 432]})
    data_mapping = ColumnMapping()
    metric = DataQualityMetrics()
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping), metrics={}
    )
    assert result is not None


def test_data_quality_stability_metrics() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [1, 1, 2, 2, 5],
            "feature2": [1, 1, 2, 2, 8],
            "target": [1, 0, 1, 1, 0],
            "prediction": [1, 0, 1, 0, 0],
        }
    )
    data_mapping = ColumnMapping()
    metric = DataQualityStabilityMetrics()
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping), metrics={}
    )
    assert result is not None
    assert result.number_not_stable_target == 2
    assert result.number_not_stable_prediction == 4


def test_data_quality_values_in_list_metrics() -> None:
    test_dataset = pd.DataFrame({"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 2, 2, 432]})
    data_mapping = ColumnMapping()
    metric = DataQualityValueListMetrics(column="category_feature", values=["d"])
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping), metrics={}
    )
    assert result is not None
    assert result.number_in_list == 1
    assert result.number_not_in_list == 3
    assert result.share_in_list == 0.25
    assert result.share_not_in_list == 0.75

    metric = DataQualityValueListMetrics(column="numerical_feature", values=[2])
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping), metrics={}
    )
    assert result is not None
    assert result.number_in_list == 2
    assert result.number_not_in_list == 2
    assert result.share_in_list == 0.5
    assert result.share_not_in_list == 0.5

    reference_dataset = pd.DataFrame({"category_feature": ["n", "y", "n", "y"], "numerical_feature": [0, 2, 2, 432]})

    metric = DataQualityValueListMetrics(column="category_feature")
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=reference_dataset, column_mapping=data_mapping),
        metrics={},
    )
    assert result is not None
    assert result.number_in_list == 2
    assert result.number_not_in_list == 2
    assert result.share_in_list == 0.5
    assert result.share_not_in_list == 0.5


def test_data_quality_values_in_list_metrics_reference_defaults() -> None:
    current_dataset = pd.DataFrame({"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 2, 2, 432]})
    reference_dataset = pd.DataFrame({"category_feature": ["n", "n", "p", "n"]})
    data_mapping = ColumnMapping()
    metric = DataQualityValueListMetrics(column="category_feature")
    result = metric.calculate(
        data=InputData(current_data=current_dataset, reference_data=reference_dataset, column_mapping=data_mapping),
        metrics={},
    )
    assert result is not None
    assert result.number_in_list == 3
    assert result.number_not_in_list == 1
    assert result.share_in_list == 0.75
    assert result.share_not_in_list == 0.25


def test_data_quality_values_in_range_metrics() -> None:
    test_dataset = pd.DataFrame({"numerical_feature": [0, 2, 2, 432]})
    data_mapping = ColumnMapping()
    metric = DataQualityValueRangeMetrics(column="numerical_feature", left=0, right=10.5)
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping), metrics={}
    )
    assert result is not None
    assert result.number_in_range == 3
    assert result.number_not_in_range == 1
    assert result.share_in_range == 0.75
    assert result.share_not_in_range == 0.25

    reference_dataset = pd.DataFrame({"numerical_feature": [0, 1, 1, 1]})

    metric = DataQualityValueRangeMetrics(column="numerical_feature")
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=reference_dataset, column_mapping=data_mapping),
        metrics={},
    )
    assert result is not None
    assert result.number_in_range == 1
    assert result.number_not_in_range == 3
    assert result.share_in_range == 0.25
    assert result.share_not_in_range == 0.75

    metric = DataQualityValueRangeMetrics(column="numerical_feature", right=5)
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=reference_dataset, column_mapping=data_mapping),
        metrics={},
    )
    assert result is not None
    assert result.number_in_range == 3
    assert result.number_not_in_range == 1
    assert result.share_in_range == 0.75
    assert result.share_not_in_range == 0.25


def test_data_quality_quantile_metrics() -> None:
    test_dataset = pd.DataFrame({"numerical_feature": [0, 2, 2, 2, 0]})
    data_mapping = ColumnMapping()
    metric = DataQualityValueQuantileMetrics(column="numerical_feature", quantile=0.5)
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping), metrics={}
    )
    assert result is not None
    assert result.quantile == 0.5
    assert result.value == 2


def test_data_quality_correlation_metrics() -> None:
    current_dataset = pd.DataFrame(
        {
            "numerical_feature_1": [0, 2, 2, 2, 0],
            "numerical_feature_2": [0, 2, 2, 2, 0],
            "category_feature": [1, 2, 4, 2, 1],
            "target": [0, 2, 2, 2, 0],
            "prediction": [0, 2, 2, 2, 0],
        }
    )
    data_mapping = ColumnMapping()
    metric = DataQualityCorrelationMetrics()
    result = metric.calculate(
        data=InputData(current_data=current_dataset, reference_data=None, column_mapping=data_mapping), metrics={}
    )
    assert result is not None
    assert result.current_correlation.num_features == ["numerical_feature_1", "numerical_feature_2", "category_feature"]
    assert result.current_correlation.correlation_matrix is not None
    assert result.current_correlation.target_prediction_correlation == 1.0
    assert result.current_correlation.abs_max_target_features_correlation == 1.0
    assert result.current_correlation.abs_max_prediction_features_correlation == 1.0
    assert result.current_correlation.abs_max_correlation == 1.0
    assert result.current_correlation.abs_max_num_features_correlation == 1.0

    assert result.reference_correlation is None
