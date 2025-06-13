# vuecore/core/plotting/plotly/converters.py
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from ....schemas.distribution.scatter import ScatterConfig


def create_plotly_scatter(data: pd.DataFrame, config: ScatterConfig) -> go.Figure:
    """
    Converts DataFrame and configuration into a Plotly scatter plot figure.

    This function acts as a bridge between the abstract plot definition and the
    Plotly Express implementation. It translates the validated configuration
    into the arguments for `plotly.express.scatter`.

    Parameters
    ----------
    data : pd.DataFrame
        The DataFrame containing the plot data.
    config : ScatterConfig
        The validated Pydantic model object containing all plot configurations.

    Returns
    -------
    go.Figure
        A `plotly.graph_objects.Figure` object representing the scatter plot.
    """
    fig = px.scatter(
        data,
        x=config.x,
        y=config.y,
        color=config.group,
        size=config.size,
        symbol=config.symbol,
        text=config.text,
        hover_data=config.hover_cols,
        color_discrete_map=config.colors,
        trendline=config.trendline,
    )
    return fig
