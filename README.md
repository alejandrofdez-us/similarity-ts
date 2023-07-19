[![version](https://img.shields.io/badge/pypi-1.0.3-blue)](https://pypi.org/project/similarity-ts/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-darkgreen)](https://www.python.org/downloads/release/python-390/)
[![last-update](https://img.shields.io/badge/last_update-07/18/2023-brightgreen)](https://github.com/alejandrofdez-us/similarity-ts-cli/commits/main)
[![license](https://img.shields.io/badge/license-MIT-orange)](LICENSE)

# SimilarityTS: Toolkit for the Evaluation of Similarity for multivariate time series

## Table of Contents

- [Package Description](#package-description)
- [Installation](#installation)
- [Usage](#usage)
- [Configuring the toolkit](#configuring-the-toolkit)
- [Extending the toolkit](#extending-the-toolkit)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Package Description

SimilarityTS is an open-source package designed to facilitate the evaluation and comparison of
multivariate time series data. It provides a comprehensive toolkit for analyzing, visualizing, and reporting multiple
metrics and figures derived from time series datasets. The toolkit simplifies the process of evaluating the similarity of
time series by offering data preprocessing, metrics computation, visualization, statistical analysis, and report generation
functionalities. With its customizable features, SimilarityTS empowers researchers and data
scientists to gain insights, identify patterns, and make informed decisions based on their time series data.

A command line interface tool is also available at: https://github.com/alejandrofdez-us/similarity-ts-cli.

### Available metrics

This toolkit can compute the following metrics:

- `kl`: Kullback-Leibler divergence
- `js`: Jensen-Shannon divergence
- `ks`: Kolmogorov-Smirnov test
- `mmd`: Maximum Mean Discrepancy
- `dtw` Dynamic Time Warping
- `cc`: Difference of co-variances
- `cp`: Difference of correlations
- `hi`: Difference of histograms

### Available figures

This toolkit can generate the following figures:

- `2d`: the ordinary graphical representation of the time series in a 2D figure with the time represented on the x axis
  and the data values on the y-axis for
    - the complete multivariate time series; and
    - a plot per column.

  Each generated figure plots both the `ts1` and the `ts2` data to easily obtain key insights into
  the similarities or differences between them.
    <div>
    <img src="https://github.com/alejandrofdez-us/similarity-ts/blob/e5b147b145970f3a93351a1004022fb30d20f5f0/docs/figures/2d_sample_3_complete_TS_1_vs_TS_2.png?raw=true" alt="2D Figure complete">
    <img src="https://github.com/alejandrofdez-us/similarity-ts/blob/e5b147b145970f3a93351a1004022fb30d20f5f0/docs/figures/2d_sample_3_cpu_util_percent_TS_1_vs_TS_2.png?raw=true" alt="2D Figure for used CPU percentage">
    </div>
- `delta`: the differences between the values of each column grouped by periods of time. For instance, the differences
  between the percentage of cpu used every 10, 25 or 50 minutes. These delta can be used as a means of comparison between
  time series short-/mid-/long-term patterns.
    <div>
    <img src="https://github.com/alejandrofdez-us/similarity-ts/blob/e5b147b145970f3a93351a1004022fb30d20f5f0/docs/figures/delta_sample_3_cpu_util_percent_TS_1_vs_TS_2_(grouped_by_10_minutes).png?raw=true" alt="Delta Figure for used CPU percentage grouped by 10 minutes">
    <img src="https://github.com/alejandrofdez-us/similarity-ts/blob/e5b147b145970f3a93351a1004022fb30d20f5f0/docs/figures/delta_sample_3_cpu_util_percent_TS_1_vs_TS_2_(grouped_by_25_minutes).png?raw=true" alt="Delta Figure for used CPU percentage grouped by 25 minutes">
    <img src="https://github.com/alejandrofdez-us/similarity-ts/blob/e5b147b145970f3a93351a1004022fb30d20f5f0/docs/figures/delta_sample_3_cpu_util_percent_TS_1_vs_TS_2_(grouped_by_50_minutes).png?raw=true" alt="Delta Figure for used CPU percentage grouped by 50 minutes">
    </div>

- `pca`: the linear dimensionality reduction technique that aims to find the principal components of a data set by
  computing the linear combinations of the original characteristics that explain the most variance in the data.
    <div align="center">
    <img src="https://github.com/alejandrofdez-us/similarity-ts/blob/e5b147b145970f3a93351a1004022fb30d20f5f0/docs/figures/PCA.png?raw=true" alt="PCA Figure" width="450">
    </div>
- `tsne`: a tool for visualising high-dimensional data sets in a 2D or 3D graphical representation allowing the creation
  of a single map that reveals the structure of the data at many different scales.
    <div align="center">
    <img src="https://github.com/alejandrofdez-us/similarity-ts/blob/e5b147b145970f3a93351a1004022fb30d20f5f0/docs/figures/t-SNE-iter_300-perplexity_5.png?raw=true" alt="TSNE Figure 300 iterations 5 perplexity" width="450">
    <img src="https://github.com/alejandrofdez-us/similarity-ts/blob/e5b147b145970f3a93351a1004022fb30d20f5f0/docs/figures/t-SNE-iter_1000-perplexity_5.png?raw=true" alt="TSNE Figure 1000 iterations 5 perplexity" width="450">
    </div>
- `dtw` path: In addition to the numerical similarity measure, the graphical representation of the DTW path of each
  column can be useful to better analyse the similarities or differences between the time series columns. Notice that
  there is no multivariate representation of DTW paths, only single column representations.
    <div>
    <img src="https://github.com/alejandrofdez-us/similarity-ts/blob/e5b147b145970f3a93351a1004022fb30d20f5f0/docs/figures/DTW_sample_3_cpu_util_percent.png?raw=true" alt="DTW Figure for cpu">
    </div>

## Installation

Install the package using pip in your local environment:

```Bash
pip install similarity-ts
```

## Usage

Users must create a new `SimilarityTs` object by calling its constructor and passing the following parameters.

- `ts1` This time series may represent the baseline or ground truth time
  series as a `numpy` array with shape `[length, num_features]`.
- `ts2s` A single or a set of time series as a `numpy` array with shape `[num_time_series, length, num_features]`.


Constraints:

- `ts1` time-series and `ts2s` time-series file(s) must:
    - have the same dimensionality (number of columns)
    - not include a timestamp column
    - include only numeric values
- all `ts2s` time-series must have the same length (number of rows).

If `ts1` time-series is longer (more rows) than `ts2s` time-series, the `ts1` time series will be
divided in windows of the same length as the `ts2s` time-series.

For each `ts2s` time-series, the most similar window (*) from `ts1` time series is selected.

Finally, metrics and figures that assess the similarity between each pair of `ts2s` time-series and its
associated most similar `ts1` window are computed.

(*) The metric used for the selection of the most
similar `ts1` time-series window per each `ts2s` time-series file is selectable. `dtw` is the default selected metric, however, any of
the
[metrics](#available-metrics) are also available for this purpose. See the [toolkit configuration section](#configuring-the-toolkit).

### Minimal usage examples:
Usage examples can be found at: https://github.com/alejandrofdez-us/similarity-ts/tree/main/usage_examples.

1. Compute metrics between random time series (`ts1`: one time series of lenght 200 and 2 dimensions and `ts2`: five time series of length 100 and 2 dimensions):
    ```Python
    import numpy as np
    from similarity_ts.similarity_ts import SimilarityTs
    
    ts1 = np.random.rand(200, 2)
    ts2s = np.random.rand(5, 100, 2)
    similarity_ts = SimilarityTs(ts1, ts2s)
    for ts2_name, metric_name, computed_metric in similarity_ts.get_metric_computer():
        print(f'{ts2_name}. {metric_name}: {computed_metric}')
    ```

1. Compute metrics and figures between random time series and save figures:
    ```Python
    import os
    import numpy as np
    from similarity_ts.plots.plot_factory import PlotFactory
    from similarity_ts.similarity_ts import SimilarityTs
    
    def main():
        ts1 = np.random.rand(200, 2)
        ts2s = np.random.rand(5, 100, 2)
        similarity_ts = SimilarityTs(ts1, ts2s)
        for ts2_name, metric_name, computed_metric in similarity_ts.get_metric_computer():
            print(f'{ts2_name}. {metric_name}: {computed_metric}')
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
    ```

## Configuring the Toolkit
Users can provide metrics or figures to be computed/generated and some other parameterisation. The following code snippet 
creates a configuration object that should be passed to the `SimilarityTs` constructor:
```Python
def __create_similarity_ts_config():
    # The list of metrics names that will be computed
    metric_config = MetricConfig(['js', 'mmd']) 
    # The list of figure names that will be generated and the time step in seconds of the time series.
    plot_config = PlotConfig(['delta', 'pca'], timestamp_frequency_seconds=300)

    # Name of each time series of the ts2s set of time series
    ts2_names = ['ts2_1_name', 'ts2_2_name', 'ts2_3_name', 'ts2_4_name', 'ts2_5_name']
    # Name of the features
    header_names = ['feature1_name', 'feature2_name']
    
    # Creation of the configuration
      # stride for cutting the ts1 when needed
      # metric used for selecting the most similar window
    similarity_ts_config = SimilarityTsConfig(metric_config, plot_config,
                                              stride=10, window_selection_metric='kl',
                                              ts2_names=ts2_names, header_names=header_names)
    return similarity_ts_config
```

If no metrics nor figures are provided, the tool will compute all the available metrics and figures.

The following arguments are also available for fine-tuning:

- `timestamp_frequency_seconds`: the frequency in seconds in which samples were taken. This is needed to generate the delta figures with correct time magnitudes. By default is
  `1` second.
- `stride`: when `ts1` time-series is longer than `ts2s` time-series the windows are computed by using a
  stride of `1` by default. Sometimes using a larger value for the stride parameter improves the performance by skipping
  the computation of similarity between so many windows.
- `window_selection_metric`: the metric used for the selection of the most similar `ts1` time-series window per each `ts2s` time-series file is selectable.`dtw` is the default selected metric, however, any of the [metrics](#available-metrics) are also available for this purpose. See the [toolkit configuration section](#configuring-the-toolkit).
- `ts2_names`: name of each time series of the `ts2s` set of time series.
- `header_names`: name of the features.


## Extending the toolkit

Additionally, users may implement their own metric or figure classes and include them by using the `MetricFactory` or `PlotFactory` register methods. To ensure compatibility with our toolkit, they have to inherit from the base classes `Metric` and `Plot`.

The following code snippet is an example of how to introduce the Euclidean distance metric:

```Python
#eu.py
import numpy as np
from similarity_ts.metrics.metric import Metric


class EuclideanDistance(Metric):

    def __init__(self):
        super().__init__()
        self.name = 'ed'

    def compute(self, ts1, ts2, similarity_ts):
        metric_result = {'Multivariate': self.__ed(ts1, ts2)}
        return metric_result

    def compute_distance(self, ts1, ts2):
        return self.__ed(ts1, ts2)

    def __ed(self, ts1, ts2):
        return np.linalg.norm(ts1 - ts2)

```

Afterward, this metric can be registered by using the `register_metric(metric_class)` method from `MetricFactory` as shown in the following code snippet:
```Python
import numpy as np
from similarity_ts.similarity_ts import SimilarityTs
from similarity_ts.metrics.metric_factory import MetricFactory
from ed import EuclideanDistance

MetricFactory.get_instance().register_metric(EuclideanDistance)
ts1 = np.random.rand(200, 2)
ts2s = np.random.rand(5, 100, 2)
similarity_ts = SimilarityTs(ts1, ts2s)
for ts2_name, metric_name, computed_metric in similarity_ts.get_metric_computer():
    print(f'{ts2_name}. {metric_name}: {computed_metric}')
```

Similarly, new plots can be introduced. For instance a `SimilarityPlotByCorrelation` could be defined as:
```Python
#cc_plot.py
import numpy as np
import matplotlib.pyplot as plt
from similarity_ts.plots.plot import Plot


class SimilarityPlotByCorrelation(Plot):

    def __init__(self, fig_size=(8, 6)):
        super().__init__(fig_size)
        self.name = 'cc-plot'

    def compute(self, similarity_ts, ts2_filename):
        super().compute(similarity_ts, ts2_filename)
        n_features = self.ts1.shape[1]
        similarity = np.corrcoef(self.ts1.T, self.ts2.T)
        fig, ax = plt.subplots()
        im = ax.imshow(similarity, cmap='RdYlBu', vmin=-1, vmax=1)
        ax.set_xticks(np.arange(n_features*2))
        ax.set_yticks(np.arange(n_features*2))
        xticklabels = [f'ts1_{nfeatures_index}'for nfeatures_index in range(1, n_features+1)]
        xticklabels = xticklabels + [f'ts2_{nfeatures_index}'for nfeatures_index in range(1, n_features+1)]
        ax.set_xticklabels(xticklabels)
        ax.set_yticklabels(xticklabels)
        ax.set_xlabel('Feature')
        ax.set_ylabel('Feature')
        for i in range(n_features*2):
            for j in range(n_features*2):
                ax.text(j, i, f'{similarity[i, j]:.2f}', ha='center', va='center', color='black')

        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel('Similarity', rotation=-90, va='bottom')
        plt.title('similarity-correlation')
        plt.tight_layout()
        return [(fig, ax)]
```

Afterward, this plot can be registered by using the `register_plot(plot_class)` method from `PlotFactory` as shown in the following code snippet that register the new metric and the new plot:
```Python
import os
import numpy as np
from similarity_ts.plots.plot_factory import PlotFactory
from similarity_ts.similarity_ts import SimilarityTs
from similarity_ts.metrics.metric_factory import MetricFactory
from ed import EuclideanDistance
from cc_plot import SimilarityPlotByCorrelation

def main():
    MetricFactory.get_instance().register_metric(EuclideanDistance)
    PlotFactory.get_instance().register_plot(SimilarityPlotByCorrelation)
    ts1 = np.random.rand(200, 2)
    ts2s = np.random.rand(5, 100, 2)
    similarity_ts = SimilarityTs(ts1, ts2s)
    for ts2_name, metric_name, computed_metric in similarity_ts.get_metric_computer():
        print(f'{ts2_name}. {metric_name}: {computed_metric}')
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
```

## License

SimilarityTS toolkit is free and open-source software licensed under the [MIT license](LICENSE).

## Acknowledgements
Project PID2021-122208OB-I00, PROYEXCEL\_00286 and  TED2021-132695B-I00 project, funded by MCIN / AEI / 10.13039 / 501100011033, by Andalusian Regional Government, and by the European Union - NextGenerationEU.
