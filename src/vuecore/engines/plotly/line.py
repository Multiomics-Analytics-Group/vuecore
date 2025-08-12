# vuecore/engines/plotly/line.py

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from vuecore.schemas.basic.line import LineConfig
from .theming import apply_line_theme


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
    # Get all parameters from the config model, including extras
    all_config_params = config.model_dump()

    # Manually define the list of parameters handled by the theme script
    # These will be removed from the initial plot_args
    theming_params = [
        "markers",
        "log_x",
        "log_y",
        "range_x",
        "range_y",
        "line_shape",
        "title",
        "subtitle",
        "template",
        "width",
        "height",
    ]

    # Create the dictionary of arguments for px.line
    plot_args = {
        k: v
        for k, v in all_config_params.items()
        if k not in theming_params and v is not None
    }

    # The fig object is created using only the arguments for px.line
    fig = px.line(data, **plot_args)

    # The theming script applies layout and style parameters after creation
    fig = apply_line_theme(fig, config)

    return fig
