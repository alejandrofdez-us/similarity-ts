import numpy as np
from .metric import Metric


class Cp(Metric):

    def __init__(self):
        super().__init__()
        self.name = 'cp'

    def compute(self, ts1, ts2, similarity_ts):
        return {'Multivariate': self.__cp(ts1, ts2)}

    def compute_distance(self, ts1, ts2):
        return self.__cp(ts1, ts2)

    def __cp(self, ts1, ts2):
        ts1_pearson = np.corrcoef(ts1, rowvar=False)
        ts2_pearson = np.corrcoef(ts2, rowvar=False)
        correlation_diff_matrix = ts1_pearson - ts2_pearson
        l1_norms_avg = np.mean([np.linalg.norm(row) for row in correlation_diff_matrix])
        return l1_norms_avg
