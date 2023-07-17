import os
from .plot import Plot
from ..helpers.dynamic_import_helper import find_available_classes


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class PlotFactory(metaclass=Singleton):
    def __init__(self, figure_names_to_be_generated):
        self.plots_to_be_generated = self.__get_plots_to_be_generated(figure_names_to_be_generated)
        self.figures_requires_all_samples = self.__get_figures_that_requires_all_samples()

    def register_plot(self, plot_class):
        new_plot = plot_class()
        self.plots_to_be_generated.append(new_plot)

    @staticmethod
    def __get_plots_to_be_generated(figure_names_to_be_generated):
        return [plot for plot_name, plot in PlotFactory.find_available_figures().items() if
                plot_name in figure_names_to_be_generated]

    @staticmethod
    def find_available_figures():
        return find_available_classes(os.path.dirname(os.path.abspath(__file__)), Plot, 'plots')

    @staticmethod
    def get_instance(figure_names_to_be_generated=None):
        if not hasattr(PlotFactory, '_instance'):
            if figure_names_to_be_generated is None:
                figure_names_to_be_generated = PlotFactory.find_available_figures().keys()
            PlotFactory._instance = PlotFactory(figure_names_to_be_generated)
        return PlotFactory._instance

    def __get_figures_that_requires_all_samples(self):
        return [plot.name for plot in self.plots_to_be_generated if
                plot.requires_all_samples()]
