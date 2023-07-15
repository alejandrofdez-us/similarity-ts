import matplotlib.pyplot as plt
import pandas
from .plot import Plot


class TwoDimensions(Plot):
    def __init__(self):
        super().__init__()
        self.seq_len = None
        self.ts2_df = None
        self.ts1_df = None
        self.name = '2d'

    def _initialize(self, similarity_ts, ts2_filename):
        super()._initialize(similarity_ts, ts2_filename)
        self.ts1_df = pandas.DataFrame(self.ts1, columns=[f'{column_name}_TS_1' for column_name in
                                                          similarity_ts.header_names])
        self.ts2_df = pandas.DataFrame(similarity_ts.ts2_dict[ts2_filename],
                                       columns=[f'{column_name}_TS_2' for column_name in
                                                similarity_ts.header_names])
        self.seq_len = similarity_ts.ts2_dict[ts2_filename].shape[0]

    def compute(self, similarity_ts, ts2_filename):
        super().compute(similarity_ts, ts2_filename)
        plot_array = [self.__generate_plot_from_df()]
        for column_index, column_name in enumerate(self.header_names):
            plot_array.append(
                self.__generate_plot_by_column(self.ts1[:, column_index], self.ts2[:, column_index], column_name))
        return plot_array

    def __generate_plot_from_df(self):
        fig, axis = super()._init_plot()
        self.ts1_df.plot(ax=axis, style='--')
        plt.gca().set_prop_cycle(None)
        self.ts2_df.plot(ax=axis)
        plt.xlim(left=0, right=len(self.ts2_df) - 1)
        super()._set_labels('complete_TS_1_vs_TS_2', 'time', 'values')
        plt.close('all')
        return fig, axis

    def __generate_plot_by_column(self, ts1_column, ts2_column, column_name):
        fig, axis = super()._init_plot()
        plt.plot(ts1_column, c='green', label='TS_1', linewidth=1)
        plt.plot(ts2_column, c='blue', label='TS_2', linewidth=2)
        plt.xlim(left=0, right=len(ts1_column) - 1)
        super()._set_labels(f'{column_name}_TS_1_vs_TS_2', 'time', column_name)
        plt.close('all')
        return fig, axis
