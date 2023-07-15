from itertools import cycle
import matplotlib.pyplot as plt
import numpy as np
from .plot import Plot


class Delta(Plot):

    def __init__(self):
        super().__init__()
        self.seq_len = None
        self.ts_freq_secs = None
        self.n_ts1_samples_to_plot = None
        self.time_magnitude = None
        self.time_magnitude_name = None
        self.name = 'delta'

    def _initialize(self, similarity_ts, ts2_filename):
        super()._initialize(similarity_ts, ts2_filename)
        self.seq_len = similarity_ts.ts2_dict[ts2_filename].shape[0]
        self.ts_freq_secs = similarity_ts.similarity_ts_config.plot_config.timestamp_frequency_seconds
        self.n_ts1_samples_to_plot = min(5, len(self.ts1_windows))
        self.time_magnitude, self.time_magnitude_name = self.__compute_time_magnitude()

    def __compute_time_magnitude(self):
        time_magnitudes = {60 * 60 * 24: 'days', 60 * 60: 'hours', 60: 'minutes'}
        selected_magnitude, selected_name = 1, 'seconds'
        for magnitude, name in time_magnitudes.items():
            if self.ts_freq_secs >= magnitude:
                selected_magnitude, selected_name = magnitude, name
                break
        return selected_magnitude, selected_name

    def compute(self, similarity_ts, ts2_filename):
        super().compute(similarity_ts, ts2_filename)
        time_intervals = [(self.ts_freq_secs / self.time_magnitude) * value for value in [2, 5, 10]]
        plot_array = []
        for column_index, column_name in enumerate(self.header_names):
            for time_interval in time_intervals:
                plot_array.append(
                    self.__generate_delta_grouped_by_interval(time_interval, column_index, column_name))
        return plot_array

    def __generate_delta_grouped_by_interval(self, time_interval, column_index, column_name):
        delta_ts1_column_array = [
            self.__compute_grouped_delta_from_sample(self.__get_random_ts1_sample(), column_index, time_interval) for _
            in
            range(self.n_ts1_samples_to_plot)]

        delta_ts2_column = self.__compute_grouped_delta_from_sample(self.ts2, column_index, time_interval)

        return self.__generate_plot(delta_ts1_column_array=delta_ts1_column_array,
                                    delta_ts2_column=delta_ts2_column, column_name=column_name,
                                    time_interval=time_interval)

    def __get_random_ts1_sample(self):
        return self.ts1_windows[np.random.randint(0, len(self.ts1_windows))]

    def __compute_grouped_delta_from_sample(self, data_sample, column_number, time_interval):
        sample_column = data_sample[:, column_number]
        seq_len = data_sample.shape[0]
        sample_column_split = np.array_split(sample_column,
                                             seq_len // (time_interval / (self.ts_freq_secs / self.time_magnitude)))
        sample_column_mean = [np.mean(batch) for batch in sample_column_split]
        delta_sample_column = -np.diff(sample_column_mean)
        return delta_sample_column

    def __generate_plot(self, delta_ts1_column_array, delta_ts2_column, column_name, time_interval):
        fig, axis = super()._init_plot()
        self.__plot_ts1_columns(delta_ts1_column_array)
        plt.plot(delta_ts2_column, c='blue', label='TS_2', linewidth=3)
        max_y = max(np.amax(delta_ts1_column_array), np.amax(delta_ts2_column))
        min_y = min(np.amin(delta_ts1_column_array), np.amin(delta_ts2_column))
        axis_limits = [0, len(delta_ts2_column) - 1, min_y, max_y]
        plt.axis(axis_limits)
        super()._set_labels(f'{column_name}_TS_1_vs_TS_2_(grouped_by_{int(time_interval)}_{self.time_magnitude_name})',
                            'time', column_name)
        plt.close('all')
        return fig, axis

    def __plot_ts1_columns(self, delta_ts1_column_array):
        cycle_colors = cycle('grcmk')
        labels = ['TS_1'] if len(delta_ts1_column_array) == 1 else [f'TS_1_sample_{i}' for i in
                                                                    range(1, len(delta_ts1_column_array) + 1)]
        for label, delta_ts1_column in zip(labels, delta_ts1_column_array):
            plt.plot(delta_ts1_column, c=next(cycle_colors), label=label, linewidth=1)
