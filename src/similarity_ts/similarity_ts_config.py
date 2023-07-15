from .metrics.metric_config import MetricConfig
from .plots.plot_config import PlotConfig


class SimilarityTsConfig:
    def __init__(self, metric_config=None, plot_config=None, stride=1, window_selection_metric='dtw', ts2_names=None,
                 header_names=None):
        if metric_config is None:
            metric_config = MetricConfig()
        if plot_config is None:
            plot_config = PlotConfig()

        self.metric_config = metric_config
        self.plot_config = plot_config
        self.stride = stride
        self.window_selection_metric = window_selection_metric
        self.ts2_names = ts2_names
        self.header_names = header_names
