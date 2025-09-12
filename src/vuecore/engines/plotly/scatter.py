import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from vuecore.schemas.basic.scatter import ScatterConfig
from vuecore.utils.statistics import get_density
from .theming import apply_scatter_theme
from .plot_builder import build_plot

# Define parameters handled by the theme script
THEMING_PARAMS = [
    "opacity",
    "log_x",
    "log_y",
    "range_x",
    "range_y",
    "title",
    "subtitle",
    "x_title",
    "y_title",
    "template",
    "width",
    "height",
    "marker_line_width",
    "marker_line_color",
    "color_by_density",
]


def scatter_preprocess(data, plot_args, config):
    """
    Preprocess data and arguments for scatter plots with density coloring.

    This function handles special preprocessing for scatter plots, particularly
    for density-based coloring.

    Parameters
    ----------
    data : pd.DataFrame
        The DataFrame containing the plot data.
    plot_args : dict
        Dictionary of arguments to be passed to the Plotly Express scatter function.
    config : ScatterConfig
        The validated Pydantic model with all scatter plot configurations.

    Returns
    -------
    tuple
        A tuple containing:
        - data : pd.DataFrame
            The original DataFrame (unchanged).
        - plot_args : dict
            The modified plot arguments dictionary with color settings adjusted
            based on the configuration.

    Notes
    -----
    When density coloring is enabled, this function calculates density values
    for the data points and uses them for color mapping, removing any discrete
    color mapping that might conflict with continuous coloring.
    """
    # Handle density coloring
    if config.color_by_density:
        # Calculate density and pass it to the 'color' argument
        density_values = get_density(data[config.x].values, data[config.y].values)
        plot_args["color"] = density_values

        # Remove discrete color mapping for density plots
        if "color_discrete_map" in plot_args:
            del plot_args["color_discrete_map"]
    else:
        # Use standard group-based coloring
        plot_args["color"] = config.color

    return data, plot_args


def build(data: pd.DataFrame, config: ScatterConfig) -> go.Figure:
    """
    Creates a Plotly scatter plot from a DataFrame and a Pydantic configuration.

    This function acts as a bridge between the abstract plot definition and the
    Plotly Express implementation. It translates the validated `ScattereConfig`
    into the arguments for `plotly.express.scatter` and also forwards any
    additional, unvalidated keyword arguments from plotly. The resulting figure
    is then customized with layout and theme settings using `plotly.graph_objects`.
    (https://plotly.com/python-api-reference/generated/plotly.express.scatter.html).

    Parameters
    ----------
    data : pd.DataFrame
        The DataFrame containing the plot data.
    config : ScatterConfig
        The validated Pydantic model object with all plot configurations.

    Returns
    -------
    go.Figure
        A `plotly.graph_objects.Figure` object representing the scatter plot.
    """
    return build_plot(
        data=data,
        config=config,
        px_function=px.scatter,
        theming_function=apply_scatter_theme,
        theming_params=THEMING_PARAMS,
        preprocess=scatter_preprocess,
    )
