import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from .dimensionalty_reduction import DimensionalityReduction


class Pca(DimensionalityReduction):

    def __init__(self):
        super().__init__()
        self.name = 'pca'

    @staticmethod
    def requires_all_samples():
        return True

    def compute(self, similarity_ts, ts2_filename):
        assert len(similarity_ts.ts1_windows) > 1, \
            'TS1 was not split. PCA needs more than 1 TS1 windows. Check TS1 size and stride parameter.'
        super().compute(similarity_ts, ts2_filename)
        pca = PCA(n_components=2)
        pca.fit(self.ts1_reduced_dimensions)
        pca_ts1 = pca.transform(self.ts1_reduced_dimensions)
        pca_ts2 = pca.transform(self.ts2_reduced_dimensions)
        fig, axis = self.__generate_plot(pca_ts1, pca_ts2)
        return [(fig, axis)]

    def __generate_plot(self, pca_ts1, pca_ts2):
        fig, axis = super()._init_plot()
        n_samples_ts1 = self.ts1_windows.shape[0]
        colors = super()._generate_colors(len(pca_ts1), len(pca_ts2))
        plt.scatter(pca_ts1[:, 0], pca_ts1[:, 1],
                    c=colors[:n_samples_ts1], alpha=0.2, label='TS_1')
        plt.scatter(pca_ts2[:, 0], pca_ts2[:, 1],
                    c=colors[n_samples_ts1:], alpha=0.2, label='TS_2')
        super()._set_labels('PCA', 'x_pca', 'y_pca')
        plt.close('all')
        return fig, axis
