from sklearn import metrics
from .metric import Metric


class Mmd(Metric):

    def __init__(self):
        super().__init__()
        self.name = 'mmd'

    def compute(self, ts1, ts2, similarity_ts):
        metric_result = {'Multivariate': self.__mmd_calculate_rbf(ts1, ts2)}
        for column_name, column_index in zip(similarity_ts.header_names, range(len(similarity_ts.header_names))):
            metric_result.update({column_name: self.__mmd_calculate_rbf(ts1[:, column_index].reshape(-1, 1),
                                                                               ts2[:, column_index].reshape(-1, 1))})
        return metric_result

    def compute_distance(self, ts1, ts2):
        return self.__mmd_calculate_rbf(ts1, ts2)

    def __mmd_calculate_rbf(self, x, y, gamma=1.0):
        xx = metrics.pairwise.rbf_kernel(x, x, gamma)
        yy = metrics.pairwise.rbf_kernel(y, y, gamma)
        xy = metrics.pairwise.rbf_kernel(x, y, gamma)
        return xx.mean() + yy.mean() - 2 * xy.mean()
