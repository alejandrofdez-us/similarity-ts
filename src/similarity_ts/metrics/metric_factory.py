import os
from .metric import Metric
from ..helpers.dynamic_import_helper import find_available_classes


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class MetricFactory(metaclass=Singleton):
    def __init__(self, metrics_names_to_be_computed):
        self.metric_objects = self.__get_metrics_to_be_computed(metrics_names_to_be_computed)

    def register_metric(self, metric_class):
        new_metric = metric_class()
        self.metric_objects.append(new_metric)

    @staticmethod
    def __get_metrics_to_be_computed(metrics_names_to_be_computed):
        return [metric for metric_name, metric in MetricFactory.find_available_metrics().items() if
                metric_name in metrics_names_to_be_computed]

    @staticmethod
    def find_available_metrics():
        return find_available_classes(os.path.dirname(os.path.abspath(__file__)), Metric, 'metrics')

    @staticmethod
    def get_metric_by_name(metric_name):
        return MetricFactory.find_available_metrics()[metric_name]

    @staticmethod
    def get_instance(metrics_to_be_computed=None):
        if not hasattr(MetricFactory, '_instance'):
            if metrics_to_be_computed is None:
                metrics_to_be_computed = MetricFactory.find_available_metrics().keys()
            MetricFactory._instance = MetricFactory(metrics_to_be_computed)
        return MetricFactory._instance
