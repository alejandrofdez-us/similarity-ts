import statistics
import scipy
from .metric import Metric

class Ks(Metric):

    def __init__(self):
        super().__init__()
        self.name = 'ks'

    def compute(self, ts1, ts2, similarity_ts):
        metric_result = {'Multivariate': self.__compute_ks(ts1, ts2)}
        for column_name, column_index in zip(similarity_ts.header_names, range(len(similarity_ts.header_names))):
            metric_result.update({column_name: self.__compute_ks(ts1[:, column_index].reshape(-1, 1), ts2[:, column_index].reshape(-1, 1))})
        return metric_result

    def compute_distance(self, ts1, ts2):
        return self.__compute_ks(ts1, ts2)

    def __compute_ks(self, ts1, ts2):
        column_indexes = range(ts2.shape[1])
        return statistics.mean(
            [scipy.stats.ks_2samp(ts2[:, column_index], ts1[:, column_index])[0] for
            column_index in column_indexes])
