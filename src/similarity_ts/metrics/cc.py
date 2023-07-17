import numpy as np
from .metric import Metric


class Cc(Metric):

    def __init__(self):
        super().__init__()
        self.name = 'cc'

    def compute(self, ts1, ts2, similarity_ts):
        metric_result = {'Multivariate': self.__cc(ts1, ts2)}
        return metric_result

    def compute_distance(self, ts1, ts2):
        return self.__cc(ts1, ts2)

    def __cc(self, ts1, ts2):
        ts1_covariance = np.cov(ts1)
        generated_data_covariance = np.cov(ts2)
        covariance_diff_matrix = ts1_covariance - generated_data_covariance
        l1_norms_avg = np.mean([np.linalg.norm(row) for row in covariance_diff_matrix])
        return l1_norms_avg
