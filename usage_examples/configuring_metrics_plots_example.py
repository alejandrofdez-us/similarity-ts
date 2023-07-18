import os
import numpy as np
from similarity_ts.metrics.metric_config import MetricConfig
from similarity_ts.plots.plot_config import PlotConfig
from similarity_ts.plots.plot_factory import PlotFactory
from similarity_ts.similarity_ts import SimilarityTs
from similarity_ts.similarity_ts_config import SimilarityTsConfig


def main():
    ts1 = np.random.rand(200, 2)
    ts2s = np.random.rand(5, 100, 2)
    similarity_ts_config = __create_similarity_ts_config()
    similarity_ts = SimilarityTs(ts1, ts2s, similarity_ts_config)
    for ts2_name, metric_name, computed_metric in similarity_ts.get_metric_computer():
        print(f'{ts2_name}. {metric_name}: {computed_metric}')
    for ts2_name, plot_name, generated_plots in similarity_ts.get_plot_computer():
        __save_figures(ts2_name, plot_name, generated_plots)

def __create_similarity_ts_config():
    metric_config = MetricConfig(['js', 'mmd'])
    plot_config = PlotConfig(['delta', 'pca'], timestamp_frequency_seconds=300)

    ts2_names = ['ts2_1_name', 'ts2_2_name', 'ts2_3_name', 'ts2_4_name', 'ts2_5_name']
    header_names = ['feature1_name', 'feature2_name']
    similarity_ts_config = SimilarityTsConfig(metric_config, plot_config,
                                              stride=10, window_selection_metric='kl',
                                              ts2_names=ts2_names, header_names=header_names)
    return similarity_ts_config

def __save_figures(filename, plot_name, generated_plots):
    for plot in generated_plots:
        dir_path = __create_directory(filename, f'figures', plot_name)
        plot[0].savefig(f'{dir_path}{plot[0].axes[0].get_title()}.pdf', format='pdf', bbox_inches='tight')


def __create_directory(filename, path, plot_name):
    if plot_name in PlotFactory.get_instance().figures_requires_all_samples:
        dir_path = f'{path}/{plot_name}/'
    else:
        original_filename = os.path.splitext(filename)[0]
        dir_path = f'{path}/{original_filename}/{plot_name}/'
    os.makedirs(dir_path, exist_ok=True)
    return dir_path

if __name__ == '__main__':
    main()