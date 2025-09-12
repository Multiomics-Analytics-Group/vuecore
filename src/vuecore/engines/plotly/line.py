# vuecore/engines/plotly/line.py

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from vuecore.schemas.basic.line import LineConfig
from .theming import apply_line_theme
from .plot_builder import build_plot

# Define parameters handled by the theme script
THEMING_PARAMS = [
    "markers",
    "log_x",
    "log_y",
    "range_x",
    "range_y",
    "line_shape",
    "title",
    "x_title",
    "y_title",
    "subtitle",
    "template",
    "width",
    "height",
]


def build(data: pd.DataFrame, config: LineConfig) -> go.Figure:
    """
    Creates a Plotly line plot figure from a DataFrame and a Pydantic configuration.

    This function acts as a bridge between the abstract plot definition and the
    Plotly Express implementation. It translates the validated `LineConfig`
    into the arguments for `plotly.express.line` and also forwards any
    additional, unvalidated keyword arguments form plotly. The resulting figure
    is then customized with layout and theme settings using `plotly.graph_objects`.
    (https://plotly.com/python-api-reference/generated/plotly.express.line.html).

    Parameters
    ----------
    data : pd.DataFrame
        The DataFrame containing the plot data.
    config : LineConfig
        The validated Pydantic model with all plot configurations.

    Returns
    -------
    go.Figure
        A `plotly.graph_objects.Figure` object representing the line plot.
    """
    return build_plot(
        data=data,
        config=config,
        px_function=px.line,
        theming_function=apply_line_theme,
        theming_params=THEMING_PARAMS,
    )
