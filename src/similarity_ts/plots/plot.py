from matplotlib import pyplot as plt


class Plot:
    @staticmethod
    def requires_all_samples():
        return False

    def __init__(self, fig_size=(18, 5)):
        self.ts2_filename = None
        self.ts1 = None
        self.ts2 = None
        self.ts1_windows = None
        self.header_names = None
        self.fig_size = fig_size

    def _initialize(self, similarity_ts, ts2_filename):
        self.ts2_filename = ts2_filename
        self.ts1 = similarity_ts.ts1_ts2_associated_windows[self.ts2_filename]['most_similar_ts1_sample']
        self.ts2 = similarity_ts.ts1_ts2_associated_windows[self.ts2_filename]['ts2']
        self.ts1_windows = similarity_ts.ts1_windows
        self.header_names = similarity_ts.header_names

    def compute(self, similarity_ts, ts2_filename):
        self._initialize(similarity_ts, ts2_filename)

    def _init_plot(self):
        plt.rcParams['figure.figsize'] = self.fig_size
        return plt.subplots(1)

    def _set_labels(self, title, x_label, y_label, ncol=None, lines=None, labels=None):
        if ncol is None:
            ncol = self.ts1.shape[1]
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        if lines and labels:
            plt.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=ncol)
        else:
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=ncol)