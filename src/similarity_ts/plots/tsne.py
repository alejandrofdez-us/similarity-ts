import itertools
import matplotlib.pyplot as plt
import numpy as np
from sklearn.manifold import TSNE
from .dimensionalty_reduction import DimensionalityReduction


class Tsne(DimensionalityReduction):

    def __init__(self):
        super().__init__()
        self.name = 'tsne'

    @staticmethod
    def requires_all_samples():
        return True

    def compute(self, similarity_ts, ts2_filename):
        super().compute(similarity_ts, ts2_filename)
        ts1_ts2_reduced_dimensions_concatenated = np.concatenate(
            (self.ts1_reduced_dimensions, self.ts2_reduced_dimensions), axis=0)
        perplexities = [5, 10, min(40, len(self.ts1_reduced_dimensions))]
        perplexities = [perplexity for perplexity in perplexities if perplexity <= len(self.ts1_reduced_dimensions)]
        iterations = [300, 1000]
        plot_array = []
        for perplexity, n_iterations in itertools.product(perplexities, iterations):
            tsne_embedding = self.__compute_tsne(ts1_ts2_reduced_dimensions_concatenated, n_iterations, perplexity)
            tsne_plot = self.__generate_plot(tsne_embedding, n_iterations, perplexity)
            plot_array.append(tsne_plot)
        return plot_array

    def __compute_tsne(self, ts1_ts2_reduced_dimensions_concatenated, n_iterations, perplexity):
        tsne = TSNE(n_components=2, verbose=0, perplexity=perplexity, n_iter=n_iterations)
        return tsne.fit_transform(ts1_ts2_reduced_dimensions_concatenated)

    def __generate_plot(self, tsne_embedding, n_iterations, perplexity):
        fig, axis = super()._init_plot()
        n_samples_ts1 = self.ts1_reduced_dimensions.shape[0]
        colors = super()._generate_colors(len(self.ts1_reduced_dimensions), len(self.ts2_reduced_dimensions))
        plt.scatter(tsne_embedding[:n_samples_ts1, 0], tsne_embedding[:n_samples_ts1, 1],
                    c=colors[:n_samples_ts1], alpha=0.2, label='TS_1')
        plt.scatter(tsne_embedding[n_samples_ts1:, 0], tsne_embedding[n_samples_ts1:, 1],
                    c=colors[n_samples_ts1:], alpha=0.2, label='TS_2')
        super()._set_labels(f't-SNE-iter_{n_iterations}-perplexity_{perplexity}', 'x_tsne', 'y_tsne')
        plt.close('all')
        return fig, axis
