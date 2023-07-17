import numpy as np
from tqdm import tqdm
from ..metrics.metric_factory import MetricFactory


def __get_most_similar_ts_sample(ts1_windows, ts2, metric_object):
    current_best = float('inf')
    most_similar_sample = []
    for ts1_window in ts1_windows:
        current_distance = metric_object.compute_distance(ts1_window, ts2)
        if metric_object.compare(current_distance, current_best) > 0:
            current_best = current_distance
            most_similar_sample = ts1_window
    return most_similar_sample


def split_ts_strided(ts_np, seq_len, stride):
    assert seq_len <= ts_np.shape[0], 'Seq_len cannot be greater than the original dataset length.'
    assert (ts_np.shape[
                0] - seq_len) >= stride - 1, 'Stride cannot be greater than the size difference between time series.'
    start_sequence_range = list(range(0, (ts_np.shape[0] - seq_len) + 1, stride))
    ts_windows = np.array(
        [ts_np[start_index:start_index + seq_len] for start_index in start_sequence_range])
    return ts_windows


def create_ts1_ts2_associated_windows(similarity_ts):
    metric_object = MetricFactory.get_metric_by_name(similarity_ts.similarity_ts_config.window_selection_metric)
    ts1_ts2_associated_windows = {}
    for filename, ts2 in tqdm(similarity_ts.ts2_dict.items(), desc='Selecting most similar windows'):
        most_similar_ts1_sample = __get_most_similar_ts_sample(similarity_ts.ts1_windows, ts2, metric_object)
        cached_metric = {similarity_ts.similarity_ts_config.window_selection_metric: metric_object.compute(most_similar_ts1_sample, ts2, similarity_ts)}
        ts1_ts2_associated_windows[filename] = {}
        ts1_ts2_associated_windows[filename]['most_similar_ts1_sample'] = most_similar_ts1_sample
        ts1_ts2_associated_windows[filename]['ts2'] = ts2
        ts1_ts2_associated_windows[filename]['cached_metric'] = cached_metric
    return ts1_ts2_associated_windows
