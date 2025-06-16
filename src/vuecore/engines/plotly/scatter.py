import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from vuecore.schemas.distribution.scatter import ScatterConfig
from vuecore.utils.statistics import get_density
from .theming import apply_scatter_theme


def build(data: pd.DataFrame, config: ScatterConfig) -> go.Figure:
    """
    Creates a Plotly scatter plot figure from a DataFrame and configuration.

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
    plot_args = {
        "x": config.x,
        "y": config.y,
        "size": config.size,
        "symbol": config.symbol,
        "text": config.text,
        "hover_data": config.hover_cols,
        "trendline": config.trendline,
    }

    if config.color_by_density:
        # Calculate density and pass it to the 'color' argument
        density_values = get_density(data[config.x].values, data[config.y].values)
        plot_args["color"] = density_values
    else:
        # Use standard group-based coloring
        plot_args["color"] = config.group
        plot_args["color_discrete_map"] = config.colors

    fig = px.scatter(data, **plot_args)

    # Apply theme right after building
    fig = apply_scatter_theme(fig, config)

    return fig
