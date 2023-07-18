import numpy as np
from similarity_ts.metrics.metric_config import MetricConfig
from similarity_ts.plots.plot_config import PlotConfig
from similarity_ts.similarity_ts import SimilarityTs
from similarity_ts.similarity_ts_config import SimilarityTsConfig


ts1 = np.random.rand(200, 2)
ts2s = np.random.rand(5, 100, 2)
similarity_ts = SimilarityTs(ts1, ts2s, similarity_ts_config)
for ts2_name, metric_name, computed_metric in similarity_ts.get_metric_computer():
    print(f'{ts2_name}. {metric_name}: {computed_metric}')