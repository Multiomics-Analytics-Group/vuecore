import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from vuecore.schemas.basic.histogram import HistogramConfig
from .theming import apply_histogram_theme
from .plot_builder import build_plot

# Define parameters handled by the theme script
THEMING_PARAMS = [
    "opacity",
    "barmode",
    "barnorm",
    "histnorm",
    "log_x",
    "log_y",
    "range_x",
    "range_y",
    "title",
    "x_title",
    "y_title",
    "subtitle",
    "template",
    "width",
    "height",
]


def build(data: pd.DataFrame, config: HistogramConfig) -> go.Figure:
    """
    Creates a Plotly histogram figure from a DataFrame and a Pydantic configuration.

    This function acts as a bridge between the abstract plot definition and the
    Plotly Express implementation. It translates the validated `HistogramConfig`
    into the arguments for `plotly.express.histogram` and also forwards any
    additional, unvalidated keyword arguments from Plotly. The resulting figure
    is then customized with layout and theme settings using `plotly.graph_objects`.
    (https://plotly.com/python-api-reference/generated/plotly.express.histogram.html).

    Parameters
    ----------
    data : pd.DataFrame
        The DataFrame containing the plot data.
    config : HistogramConfig
        The validated Pydantic model with all plot configurations.

    Returns
    -------
    go.Figure
        A `plotly.graph_objects.Figure` object representing the histogram.
    """
    return build_plot(
        data=data,
        config=config,
        px_function=px.histogram,
        theming_function=apply_histogram_theme,
        theming_params=THEMING_PARAMS,
    )
