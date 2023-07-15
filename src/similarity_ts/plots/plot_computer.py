import warnings
from ..similarity_analysis_computer import SimilarityAnalysisComputer


class PlotComputer(SimilarityAnalysisComputer):
    def __init__(self, similarity_ts, analysis):
        super().__init__(similarity_ts, analysis)
        self.already_computed_figures_requires_all_samples = []

    def _compute_next_analysis(self):
        plot = next(self.analysis_iterator)
        ts2_filename, _ = self.current_associated_window
        computed_plots = []
        if plot.name not in self.already_computed_figures_requires_all_samples:
            try:
                if plot.requires_all_samples():
                    self.already_computed_figures_requires_all_samples.append(plot.name)
                computed_plots = plot.compute(self.similarity_ts, ts2_filename)
            except Exception as e:
                warnings.warn(f'Warning: Plot {plot.name} could not be computed. Details: {e}', Warning)
        return ts2_filename, plot.name, computed_plots
