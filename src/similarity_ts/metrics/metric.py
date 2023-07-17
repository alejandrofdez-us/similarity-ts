class Metric:

    def compute(self, ts1, ts2, similarity_ts):
        raise NotImplementedError('Subclasses must implement compute() method')

    def compute_distance(self, ts1, ts2):
        raise NotImplementedError('Subclasses must implement compute_distance() method')

    def compare(self, metric1, metric2):
        return metric2 - metric1
