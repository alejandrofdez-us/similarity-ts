import numpy as np
import matplotlib.pyplot as plt
from similarity_ts.plots.plot import Plot


class SimilarityPlotByCorrelation(Plot):

    def __init__(self, fig_size=(8, 6)):
        super().__init__(fig_size)
        self.name = 'cc-plot'

    def compute(self, similarity_ts, ts2_filename):
        super().compute(similarity_ts, ts2_filename)
        n_features = self.ts1.shape[1]
        similarity = np.corrcoef(self.ts1.T, self.ts2.T)
        fig, ax = plt.subplots()
        im = ax.imshow(similarity, cmap='RdYlBu', vmin=-1, vmax=1)
        ax.set_xticks(np.arange(n_features*2))
        ax.set_yticks(np.arange(n_features*2))
        xticklabels = [f'ts1_{nfeatures_index}'for nfeatures_index in range(1, n_features+1)]
        xticklabels = xticklabels + [f'ts2_{nfeatures_index}'for nfeatures_index in range(1, n_features+1)]
        ax.set_xticklabels(xticklabels)
        ax.set_yticklabels(xticklabels)
        ax.set_xlabel('Feature')
        ax.set_ylabel('Feature')
        for i in range(n_features*2):
            for j in range(n_features*2):
                ax.text(j, i, f'{similarity[i, j]:.2f}', ha='center', va='center', color='black')

        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel('Similarity', rotation=-90, va='bottom')
        plt.title('similarity-correlation')
        plt.tight_layout()
        return [(fig, ax)]
