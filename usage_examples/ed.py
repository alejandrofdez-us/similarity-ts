import numpy as np
from similarity_ts.metrics.metric import Metric


class EuclideanDistance(Metric):

    def __init__(self):
        super().__init__()
        self.name = 'ed'

    def compute(self, ts1, ts2, similarity_ts):
        metric_result = {'Multivariate': self.__ed(ts1, ts2)}
        return metric_result

    def compute_distance(self, ts1, ts2):
        return self.__ed(ts1, ts2)

    def __ed(self, ts1, ts2):
        return np.linalg.norm(ts1 - ts2)
