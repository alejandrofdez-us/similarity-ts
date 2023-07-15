import statistics
import scipy
from .metric import Metric

class Ks(Metric):

    def __init__(self):
        super().__init__()
        self.name = 'ks'

    def compute(self, ts1, ts2):
        metric_result = {'Multivariate': self.__compute_ks(ts1, ts2)}

        for column in range(ts2.shape[1]):
            metric_result.update({f'Column_{column}': self.__compute_ks(ts1[:, column].reshape(-1, 1), ts2[:, column].reshape(-1, 1))})

        return metric_result

    def compute_distance(self, ts1, ts2):
        return self.__compute_ks(ts1, ts2)

    def __compute_ks(self, ts1, ts2):
        column_indexes = range(ts2.shape[1])
        return statistics.mean(
            [scipy.stats.ks_2samp(ts2[:, column_index], ts1[:, column_index])[0] for
            column_index in column_indexes])
