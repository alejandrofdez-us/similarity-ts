from .kl import Kl
from .metric import Metric


class Js(Metric):

    def __init__(self):
        super().__init__()
        self.name = 'js'

    def compute(self, ts1, ts2, similarity_ts):
        metric_result = {'Multivariate': self.__js_distance_multivariate(ts1, ts2)}
        for column_name, column_index in zip(similarity_ts.header_names, range(len(similarity_ts.header_names))):
            metric_result.update(
                {column_name: self.__js_distance(ts1[:, column_index].reshape(-1, 1), ts2[:, column_index].reshape(-1, 1))})
        return metric_result

    def compute_distance(self, ts1, ts2):
        return self.__js_distance_multivariate(ts1, ts2)

    def __js_distance(self, ts1, ts2, num_bins=100):
        kl_p_m, kl_q_m = Kl.kl_divergence_univariate(ts1, ts2, num_bins=num_bins)
        return (kl_p_m + kl_q_m) / 2

    def __js_distance_multivariate(self, ts1, ts2):
        kl_divergence_1 = Kl.kl_divergence(ts1, ts2)
        kl_divergence_2 = Kl.kl_divergence(ts2, ts1)
        return (kl_divergence_1 + kl_divergence_2) / 2
