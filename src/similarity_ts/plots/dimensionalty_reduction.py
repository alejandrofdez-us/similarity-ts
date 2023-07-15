import numpy as np
from .plot import Plot


class DimensionalityReduction(Plot):
    def __init__(self, fig_size=(8, 6)):
        super().__init__(fig_size)
        self.ts1_reduced_dimensions = None
        self.ts2_reduced_dimensions = None

    def _initialize(self, similarity_ts, ts2_filename):
        super()._initialize(similarity_ts, ts2_filename)
        self.ts1_reduced_dimensions, self.ts2_reduced_dimensions = self.__reduce_tss_dimensionality(
            similarity_ts.ts1_windows,
            np.asarray(similarity_ts.ts2s))

    def __reduce_tss_dimensionality(self, ts1, ts2):
        ts1_reduced = self.__reduce_ts_dimensionality(ts1)
        ts2_reduced = self.__reduce_ts_dimensionality(ts2)
        return ts1_reduced, ts2_reduced

    def __reduce_ts_dimensionality(self, ts):
        n_samples, n_steps, n_features = ts.shape
        return np.reshape(ts, (n_samples, n_steps * n_features))

    def _generate_colors(self, color1_size, color2_size):
        return ['red' for _ in range(color1_size)] + ['blue' for _ in range(color2_size)]
