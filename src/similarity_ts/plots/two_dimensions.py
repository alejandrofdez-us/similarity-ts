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
        lines1, labels1 = self.__get_lines_and_labels_from_plot(self.ts1_df, axis, style='--')
        plt.gca().set_prop_cycle(None)
        lines2, labels2 = self.__get_lines_and_labels_from_plot(self.ts2_df, axis)
        interleaved_lines = self.__interleave_lists(lines1, lines2)
        interleaved_labels = self.__interleave_lists(labels1, labels2)
        plt.xlim(left=0, right=len(self.ts2_df) - 1)
        super()._set_labels('complete_TS_1_vs_TS_2', 'time', 'values', ncol=len(lines1), lines=interleaved_lines,
                            labels=interleaved_labels)
        plt.close('all')
        return fig, axis

    def __get_lines_and_labels_from_plot(self, dataframe, axis, style=None):
        plot_lines = dataframe.plot(ax=axis, style=style).lines[-len(dataframe.columns):]
        plot_labels = dataframe.columns.tolist()
        return plot_lines, plot_labels

    def __interleave_lists(self, list1, list2):
        interleaved_list = [None] * (len(list1) + len(list2))
        interleaved_list[::2] = list1
        interleaved_list[1::2] = list2
        return interleaved_list

    def __generate_plot_by_column(self, ts1_column, ts2_column, column_name):
        fig, axis = super()._init_plot()
        plt.plot(ts1_column, c='green', label='TS_1', linewidth=1)
        plt.plot(ts2_column, c='blue', label='TS_2', linewidth=2)
        plt.xlim(left=0, right=len(ts1_column) - 1)
        super()._set_labels(f'{column_name}_TS_1_vs_TS_2', 'time', column_name, ncol=2)
        plt.close('all')
        return fig, axis
