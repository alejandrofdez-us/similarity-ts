import os
import numpy as np
from similarity_ts.plots.plot_factory import PlotFactory
from similarity_ts.similarity_ts import SimilarityTs

def main():
    ts1 = np.random.rand(200, 2)
    ts2s = np.random.rand(5, 100, 2)
    similarity_ts = SimilarityTs(ts1, ts2s)
    for ts2_name, plot_name, generated_plots in similarity_ts.get_plot_computer():
        __save_figures(ts2_name, plot_name, generated_plots)


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