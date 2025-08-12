import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from vuecore.schemas.basic.scatter import ScatterConfig
from vuecore.utils.statistics import get_density

from .theming import apply_scatter_theme


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
    # Get all parameters from the config model, including extras
    all_config_params = config.model_dump()

    # Define parameters handled by the theme script
    theming_params = [
        "opacity",
        "size_max",
        "log_x",
        "log_y",
        "range_x",
        "range_y",
        "title",
        "subtitle",
        "template",
        "width",
        "height",
        "marker_line_width",
        "marker_line_color",
        "color_by_density",
    ]

    # Create the dictionary of arguments for px.scatter
    plot_args = {
        k: v
        for k, v in all_config_params.items()
        if k not in theming_params and v is not None
    }

    # Handle density coloring separately
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

    # Create the base figure using only the arguments for px.scatter
    fig = px.scatter(data, **plot_args)

    # Apply theme and additional styling
    fig = apply_scatter_theme(fig, config)

    return fig
