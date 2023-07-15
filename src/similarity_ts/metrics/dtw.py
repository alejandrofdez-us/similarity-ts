import numpy as np
from dtaidistance import dtw_ndim
from .metric import Metric


class Dtw(Metric):

    def __init__(self):
        super().__init__()
        self.name = 'dtw'

    def compute(self, ts1, ts2):
        metric_result = {'Multivariate': self.__compute_dtw(ts1, ts2)}
        for column in range(ts2.shape[1]):
            metric_result.update(
                {f'Column_{column}': self.__compute_dtw(ts1[:, column].reshape(-1, 1), ts2[:, column].reshape(-1, 1))})
        return metric_result

    def compute_distance(self, ts1, ts2):
        return self.__compute_dtw(ts1, ts2)

    def __compute_dtw(self, ts1, ts2):
        sample_length = len(ts2)
        processed_ts2 = np.insert(ts2, 0, np.ones(sample_length, dtype=int), axis=1)
        processed_ts2 = np.insert(processed_ts2, 0, range(sample_length), axis=1)
        processed_ts1 = np.insert(ts1, 0, np.ones(sample_length, dtype=int), axis=1)
        processed_ts1 = np.insert(processed_ts1, 0, range(sample_length), axis=1)

        return dtw_ndim.distance_fast(processed_ts2, processed_ts1)
