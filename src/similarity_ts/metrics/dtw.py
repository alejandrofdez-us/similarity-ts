import numpy as np
from dtaidistance import dtw_ndim
from .metric import Metric


class Dtw(Metric):

    def __init__(self):
        super().__init__()
        self.name = 'dtw'

    def compute(self, ts1, ts2, similarity_ts):
        metric_result = {'Multivariate': self.__compute_dtw(ts1, ts2)}
        for column_name, column_index in zip(similarity_ts.header_names, range(len(similarity_ts.header_names))):
            metric_result.update(
                {column_name: self.__compute_dtw(ts1[:, column_index].reshape(-1, 1), ts2[:, column_index].reshape(-1, 1))})
        return metric_result

    def compute_distance(self, ts1, ts2):
        return self.__compute_dtw(ts1, ts2)

    def __compute_dtw(self, ts1, ts2):
        return dtw_ndim.distance_fast(ts2, ts1)
