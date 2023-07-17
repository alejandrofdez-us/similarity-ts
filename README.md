[![version](https://img.shields.io/badge/version-2.0-blue)](https://github.com/alejandrofdez-us/TimeSeriesEvaluationFramework/releases)
[![Python 3.9](https://img.shields.io/badge/python-3.9-darkgreen)](https://www.python.org/downloads/release/python-390/)
[![last-update](https://img.shields.io/badge/last_update-07/XY/2023-brightgreen)](https://github.com/alejandrofdez-us/TimeSeriesEvaluationFramework/commits/main)
![license](https://img.shields.io/badge/license-MIT-orange)

# SimilarityTS: Toolkit for the Evaluation of Similarity for multivariate time series

## Table of Contents

- [Project Description](#project-description)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Project Description

SimilarityTS is an open-source project designed to facilitate the evaluation and comparison of
multivariate time series data. It provides a comprehensive toolkit for analyzing, visualizing, and reporting multiple
metrics and figures derived from time series datasets. The toolkit simplifies the process of evaluating the similarity of
time series by offering data preprocessing, metrics computation, visualization, statistical analysis, and report generation
functionalities. With its customizable features, SimilarityTS empowers researchers and data
scientists to gain insights, identify patterns, and make informed decisions based on their time series data.

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

- `2D`: the ordinary graphical representation of the time series in a 2D figure with the time represented on the x axis
  and the data values on the y-axis for
    - the complete multivariate time series; and
    - a plot per column.

  Each generated figure plots both the original and the synthetically generated data to easily obtain key insights into
  the similarities or differences between them.
- `delta`: the differences between the values of each column grouped by periods of time. For instance, the differences
  between the cpu usage every 5 minutes or every 30 minutes. These delta can be used as a means of comparison between
  time series short-/mid-/long-term patterns.
  ![Delta Image grouped by 2 minutes](docs/images/mini_sample_1/delta/cpu_TS_1_vs_TS_2_(grouped_by_2_minutes).png)
  ![Delta Image grouped by 5 minutes](docs/images/mini_sample_1/delta/cpu_TS_1_vs_TS_2_(grouped_by_5_minutes).png)
  ![Delta Image grouped by 10 minutes](docs/images/mini_sample_1/delta/cpu_TS_1_vs_TS_2_(grouped_by_10_minutes).png)
- `pca`: the linear dimensionality reduction technique that aims to find the principal components of a data set by
  computing the linear combinations of the original characteristics that explain the most variance in the data.
  ![PCA Image](docs/images/pca/PCA.png)
- `tsne`: a tool for visualising high-dimensional data sets in a 2D or 3D graphical representation allowing the creation
  of a single map that reveals the structure of the data at many different scales.
  ![TSNE Image 300 iterations 40 perplexity](docs/images/tsne/t_SNE_iter_300-perplexity_40.png)
  ![TSNE Image 1000 iterations 40 perplexity](docs/images/tsne/t_SNE_iter_1000-perplexity_40.png)
- `dtw` path: In addition to the numerical similarity measure, the graphical representation of the DTW path of each
  column can be useful to better analyse the similarities or differences between the time series columns. Notice that
  there is no multivariate representation of DTW paths, only single column representations.
  ![DTW Image for cpu](docs/images/mini_sample_1/dtw/DTW_cpu.png)

## Installation

Install the package using pip in your local environment:

```Bash
pip install similarity-ts
```

## Usage

Users must provide numpy objects containing multivariate time series.

- `-ts1` should point to a single `csv` filename. This time series may represent the baseline or ground truth time
  series.
- `-ts2_path` can point to another single `csv` filename or a directory that contains multiple `csv` files to be
  compared with `-ts1` file.
- `-head` if your time series files include a header this argument must be present. If not present, the software
  understands that csv files don't include a header row.

Constraints:

- `-ts1` time-series file and `-ts2_path` time-series file(s) must:
    - have the same dimensionality (number of columns)
    - not include a timestamp column
    - include only numeric values
    - include the same header (if present)
- if a header is present as first row, use the `-head` argument
- all `-ts2_path` time-series files must have the same length (number of rows).

Note: the column delimiter is automatically detected.

If `-ts1` time-series file is longer (more rows) than `-ts2_path` time-series file(s), the `-ts1` time series will be
divided in windows of the same
length as the `-ts2_path` time-series file(s).

For each `-ts2_path` time-series file, the most similar window (*) from `-ts1` time series is selected.

Finally, metrics and figures that assess the similarity between each pair of `-ts2_path` time-series file and its
associated most similar `-ts1` window are computed.

(*) `-w_select_met` is the metric used for the selection of the most
similar `-ts1` time-series window per each `--ts2_path` time-series file(s).`dtw` is the default value, however, any of
the
[metrics](#available-metrics) are also available for this purpose using this argument.

Users can provide metrics or figures to be computed/generated:

- `-m` the [metrics](#available-metrics) names to be computed as a list separated by spaces.
- `-f` the [figures](#available-figures) names to be computed as a list separated by spaces

If no metrics nor figures are provided, the tool will compute all the available metrics and figures.

The following arguments are also available for fine-tuning:

- `-ts_freq_secs` the frequency in seconds in which samples were taken just to generate the delta figures. By default is
  `1` second.
- `-strd` when `ts1` time-series is longer than `ts2_path` time-series file(s) the windows are computed by using a
  stride of `1` by default. Sometimes using a larger value for the stride parameter improves the performance by skipping
  the computation of similarity between so many windows.

### Minimal usage examples:

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
### Customised usage
TODO: include some examples reading csv files and creating metrics and plots configs.

## Extending the toolkit

Additionally, users may implement their own metric or figure classes and include them by using the `MetricFactory` or `PlotFactory` register methods. To ensure compatibility with our framework, they have to inherit from the base classes (`Metric` and `Plot`).

The following code snippet is an example of how to introduce the Euclidean disntance metric:

```Python
import numpy as np
from .metric import Metric


class EuclideanDistance(Metric):

    def __init__(self):
        super().__init__()
        self.name = 'eu'

    def compute(self, ts1, ts2):
        metric_result = {'Multivariate': self.__eu(ts1, ts2)}
        return metric_result

    def compute_distance(self, ts1, ts2):
        return self.__eu(ts1, ts2)

    def __eu(self, ts1, ts2):
        return np.linalg.norm(ts1 - ts2)
```

This allows the toolkit to dynamically recognize and utilize these custom classes based on user input. By cloning the GitHub repository and including
them in the `metrics` folder, users can easily include their custom metrics when running the toolkit.

## License

Time Series Evaluation Framework is free and open-source software licensed under the [MIT license](LICENSE).