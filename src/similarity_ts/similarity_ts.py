from .similarity_ts_config import SimilarityTsConfig
from .metrics.metric_computer import MetricComputer
from .metrics.metric_factory import MetricFactory
from .plots.plot_computer import PlotComputer
from .plots.plot_factory import PlotFactory
from .helpers.window_sampler import create_ts1_ts2_associated_windows, split_ts_strided


class SimilarityTs:
    def __init__(self, ts1, ts2s, similarity_ts_config=None):
        self.ts1 = ts1
        self.ts2s = ts2s
        self.similarity_ts_config = similarity_ts_config if similarity_ts_config is not None else SimilarityTsConfig()
        self.header_names = self.similarity_ts_config.header_names if self.similarity_ts_config.header_names is not None else [
            'column-' + str(i)
            for i in
            range(ts1.shape[1])]
        self.ts2_dict = self.__build_ts2_dict(self.ts2s, self.similarity_ts_config.ts2_names)
        self.ts1_windows = split_ts_strided(self.ts1, self.ts2s[0].shape[0], self.similarity_ts_config.stride)
        self.ts1_ts2_associated_windows = create_ts1_ts2_associated_windows(self)
        self.metric_factory = MetricFactory.get_instance(self.similarity_ts_config.metric_config.metrics)
        self.plot_factory = PlotFactory.get_instance(self.similarity_ts_config.plot_config.figures)


    def __build_ts2_dict(self, ts2s, ts2_filenames):
        ts2_filenames = ts2_filenames if ts2_filenames is not None else ['ts2_' + str(i) for i in range(len(ts2s))]
        return {ts2_name: ts2 for ts2, ts2_name in zip(ts2s, ts2_filenames)}

    def get_metric_computer(self):
        return MetricComputer(self, self.metric_factory.metric_objects)

    def get_plot_computer(self):
        return PlotComputer(self, self.plot_factory.plots_to_be_generated)
