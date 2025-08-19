# vuecore/engines/plotly/bar.py

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from vuecore.schemas.basic.bar import BarConfig
from .theming import apply_bar_theme


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
    # Get all parameters from the config model, including extras
    all_config_params = config.model_dump()

    # Define parameters handled by the theme script
    # These parameters often control layout and styling aspects
    # that are better managed centrally by a theming function.
    theming_params = [
        "opacity",
        "orientation",
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

    # Create the dictionary of arguments for px.bar
    plot_args = {
        k: v
        for k, v in all_config_params.items()
        if k not in theming_params and v is not None
    }

    # Create the base figure using only the arguments relevant to px.bar
    fig = px.bar(data, **plot_args)

    # Apply theme and additional styling to the generated figure.
    fig = apply_bar_theme(fig, config)

    return fig
