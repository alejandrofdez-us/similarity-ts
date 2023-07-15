from .metric_factory import MetricFactory


class MetricConfig:
    def __init__(self, metrics_names_to_be_computed=None):
        if metrics_names_to_be_computed is None:
            metrics_names_to_be_computed = MetricFactory.find_available_metrics().keys()
        self.metrics = metrics_names_to_be_computed
