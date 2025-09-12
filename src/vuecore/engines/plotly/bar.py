# vuecore/engines/plotly/bar.py

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from vuecore.schemas.basic.bar import BarConfig
from .theming import apply_bar_theme
from .plot_builder import build_plot

# Define parameters handled by the theme script
THEMING_PARAMS = [
    "opacity",
    "barmode",
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


def build(data: pd.DataFrame, config: BarConfig) -> go.Figure:
    """
    Creates a Plotly bar plot figure from a DataFrame and a Pydantic configuration.

    This function acts as a bridge between the abstract plot definition and the
    Plotly Express implementation. It translates the validated `BarConfig`
    into the arguments for `plotly.express.bar` and also forwards any
    additional, unvalidated keyword arguments from Plotly. The resulting figure
    is then customized with layout and theme settings using `plotly.graph_objects`.
    (https://plotly.com/python-api-reference/generated/plotly.express.bar.html).

    Parameters
    ----------
    data : pd.DataFrame
        The DataFrame containing the plot data.
    config : BarConfig
        The validated Pydantic model with all plot configurations.

    Returns
    -------
    go.Figure
        A `plotly.graph_objects.Figure` object representing the bar plot.
    """
    return build_plot(
        data=data,
        config=config,
        px_function=px.bar,
        theming_function=apply_bar_theme,
        theming_params=THEMING_PARAMS,
    )
