# vuecore/engines/plotly/box.py

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from vuecore.schemas.basic.box import BoxConfig
from .theming import apply_box_theme


def build(data: pd.DataFrame, config: BoxConfig) -> go.Figure:
    """
    Creates a Plotly box plot figure from a DataFrame and a Pydantic configuration.

    This function acts as a bridge between the abstract plot definition and the
    Plotly Express implementation. It translates the validated `BoxConfig`
    into the arguments for `plotly.express.box` and also forwards any
    additional, unvalidated keyword arguments from Plotly. The resulting figure
    is then customized with layout and theme settings using `plotly.graph_objects`.
    (https://plotly.com/python-api-reference/generated/plotly.express.box.html).

    Parameters
    ----------
    data : pd.DataFrame
        The DataFrame containing the plot data.
    config : BoxConfig
        The validated Pydantic model with all plot configurations.

    Returns
    -------
    go.Figure
        A `plotly.graph_objects.Figure` object representing the box plot.
    """
    # Get all parameters from the config model, including extras
    all_config_params = config.model_dump()

    # Define parameters handled by the theme script
    theming_params = [
        "boxmode",
        "log_x",
        "log_y",
        "range_x",
        "range_y",
        "notched",
        "points",
        "title",
        "x_title",
        "y_title",
        "subtitle",
        "template",
        "width",
        "height",
    ]

    # Create the dictionary of arguments for px.box
    plot_args = {
        k: v
        for k, v in all_config_params.items()
        if k not in theming_params and v is not None
    }

    # Create the base figure using only the arguments relevant to px.box
    fig = px.box(data, **plot_args)

    # Apply theme and additional styling to the generated figure.
    fig = apply_box_theme(fig, config)

    return fig
