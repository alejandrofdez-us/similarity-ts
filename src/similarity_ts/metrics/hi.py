import numpy as np
from .metric import Metric


class Hi(Metric):

    def __init__(self):
        super().__init__()
        self.name = 'hi'

    def compute(self, ts1, ts2, similarity_ts):
        metric_result = {'Multivariate': self.__compute_hi(ts1, ts2)}
        for column_name, column_index in zip(similarity_ts.header_names, range(len(similarity_ts.header_names))):
            metric_result.update(
                {column_name: self.__compute_hi(ts1[:, column_index].reshape(-1, 1), ts2[:, column_index].reshape(-1, 1))})
        return metric_result

    def compute_distance(self, ts1, ts2):
        return self.__compute_hi(ts1, ts2)

    def __compute_hi(self, ts1, ts2):
        histogram_diff_matrix = []
        for column in range(0, ts1.shape[1]):
            ts1_column_values = ts1[:, column]
            ts1_histogram, _ = np.histogram(ts1_column_values)
            generated_data_column_values = ts2[:, column]
            generated_histogram, _ = np.histogram(generated_data_column_values)
            column_histogram_diff = ts1_histogram - generated_histogram
            histogram_diff_matrix.append(column_histogram_diff)
        histogram_diff_matrix = np.asmatrix(histogram_diff_matrix)
        l1_norms_histogram_diff = np.apply_along_axis(np.linalg.norm, 1, histogram_diff_matrix)

        l1_norms_histogram_diff_avg = l1_norms_histogram_diff.mean()

        return l1_norms_histogram_diff_avg
