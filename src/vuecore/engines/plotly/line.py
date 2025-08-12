# vuecore/engines/plotly/line.py

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from vuecore.schemas.basic.line import LineConfig
from .theming import apply_line_theme


def build(data: pd.DataFrame, config: LineConfig) -> go.Figure:
    """
    Creates a Plotly line plot figure from a DataFrame and configuration.

    This function acts as a bridge between the abstract plot definition and the
    Plotly Express implementation. It translates the validated `LineConfig`
    into the arguments for `plotly.express.line`
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
    # Arguments for mapping data to visual properties
    plot_args = {
        "x": config.x,
        "y": config.y,
        "line_group": config.line_group,
        "color": config.color,
        "line_dash": config.line_dash,
        "symbol": config.symbol,
        "hover_name": config.hover_name,
        "hover_data": config.hover_data,
        "text": config.text,
        "error_x": config.error_x,
        "error_y": config.error_y,
        "labels": config.labels,
        "facet_row": config.facet_row,
        "facet_col": config.facet_col,
        "color_discrete_map": config.color_discrete_map,
        "line_dash_map": config.line_dash_map,
        "symbol_map": config.symbol_map,
    }

    # Filter out None values to avoid passing them to Plotly
    plot_args = {k: v for k, v in plot_args.items() if v is not None}

    fig = px.line(data, **plot_args)

    # Apply theme
    fig = apply_line_theme(fig, config)

    return fig
