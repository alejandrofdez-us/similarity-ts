from .plot_factory import PlotFactory


class PlotConfig:
    def __init__(self, figure_names_to_be_generated=None, timestamp_frequency_seconds=1):
        assert timestamp_frequency_seconds > 0, 'Timestamp frequency seconds must be greater than 0'
        if figure_names_to_be_generated is None:
            figure_names_to_be_generated = PlotFactory.find_available_figures().keys()
        self.figures = figure_names_to_be_generated
        self.timestamp_frequency_seconds = timestamp_frequency_seconds
