import plotly.graph_objects as go

from vuecore.schemas.basic.scatter import ScatterConfig
from vuecore.schemas.basic.line import LineConfig
from vuecore.schemas.basic.bar import BarConfig
from vuecore.schemas.basic.box import BoxConfig


def _get_axis_title(config, axis: str) -> str:
    """
    Helper function to get axis title from configuration with appropriate fallbacks.

    This function attempts to retrieve an axis title using the following priority:
    1. Explicit axis title if provided in configuration
    2. Label mapping from configuration if available
    3. Title-cased column name as fallback

    Parameters
    ----------
    config : Any
        The configuration object containing styling and layout information.
    axis : str
        The axis identifier ('x' or 'y').

    Returns
    -------
    str
        The appropriate title for the specified axis.
    """
    axis_title_attr = f"{axis}_title"
    axis_value_attr = axis

    # Use explicit title if provided
    if getattr(config, axis_title_attr):
        return getattr(config, axis_title_attr)

    # Use label mapping if available
    if config.labels and getattr(config, axis_value_attr):
        axis_value = getattr(config, axis_value_attr)
        if axis_value in config.labels:
            return config.labels[axis_value]

    # Fall back to title-cased column name
    if getattr(config, axis_value_attr):
        return getattr(config, axis_value_attr).title()

    return ""


def _apply_common_layout(fig: go.Figure, config) -> go.Figure:
    """
    Applies common layout settings to a Plotly figure.

    This function handles the layout adjustments that are common across
    different plot types, such as titles, dimensions, templates, and axis
    properties.

    Parameters
    ----------
    fig : go.Figure
        The Plotly figure object to be styled.
    config : Any
        The configuration object containing all styling and layout information.

    Returns
    -------
    go.Figure
        The Plotly figure with common layout settings applied.
    """
    x_title = _get_axis_title(config, "x")
    y_title = _get_axis_title(config, "y")

    layout_updates = {
        "title_text": config.title,
        "title_subtitle_text": config.subtitle,
        "xaxis_title": x_title,
        "yaxis_title": y_title,
        "height": config.height,
        "width": config.width,
        "template": config.template,
        "xaxis_type": "log" if config.log_x else None,
        "yaxis_type": "log" if config.log_y else None,
        "xaxis_range": config.range_x,
        "yaxis_range": config.range_y,
    }

    fig.update_layout(**{k: v for k, v in layout_updates.items() if v is not None})
    return fig


def apply_scatter_theme(fig: go.Figure, config: ScatterConfig) -> go.Figure:
    """
    Applies a consistent layout and theme to a Plotly scatter plot.

    This function handles all styling and layout adjustments, such as titles,
    dimensions, templates, and trace properties, separating these concerns
    from the initial data mapping.

    Parameters
    ----------
    fig : go.Figure
        The Plotly figure object to be styled.
    config : ScatterConfig
        The configuration object containing all styling and layout info.

    Returns
    -------
    go.Figure
        The styled Plotly figure object.
    """
    # Apply trace-specific updates
    fig.update_traces(
        marker=dict(
            opacity=config.opacity,
            line=dict(width=config.marker_line_width, color=config.marker_line_color),
        ),
        selector=dict(mode="markers"),
    )

    # Apply common layout
    fig = _apply_common_layout(fig, config)

    return fig


def apply_line_theme(fig: go.Figure, config: LineConfig) -> go.Figure:
    """
    Applies a consistent layout and theme to a Plotly line plot.

    This function handles all styling and layout adjustments, such as titles,
    dimensions, templates, and trace properties, separating these concerns
    from the initial data mapping.

    Parameters
    ----------
    fig : go.Figure
        The Plotly figure object to be styled.
    config : LineConfig
        The configuration object containing all styling and layout info.

    Returns
    -------
    go.Figure
        The styled Plotly figure object.
    """
    # Apply trace-specific updates
    fig.update_traces(
        mode="lines+markers" if config.markers else "lines",
        line_shape=config.line_shape,
    )

    # Use the labels dictionary to set axis titles, falling back to defaults
    x_title = config.x_title or (
        config.labels.get(config.x) if config.labels else None or config.x.title()
    )
    y_title = config.y_title or (
        config.labels.get(config.y) if config.labels else None or config.y.title()
    )

    # Apply common layout
    fig = _apply_common_layout(fig, config)

    return fig


def apply_bar_theme(fig: go.Figure, config: BarConfig) -> go.Figure:
    """
    Applies a consistent layout and theme to a Plotly bar plot.

    This function handles all styling and layout adjustments, such as titles,
    dimensions, templates, and trace properties, separating these concerns
    from the initial data mapping.

    Parameters
    ----------
    fig : go.Figure
        The Plotly figure object to be styled.
    config : BarConfig
        The configuration object containing all styling and layout info.

    Returns
    -------
    go.Figure
        The styled Plotly figure object.
    """
    # Apply trace-specific updates for bar plots
    fig.update_traces(opacity=config.opacity, selector=dict(type="bar"))

    # Apply common layout
    fig = _apply_common_layout(fig, config)

    return fig


def apply_box_theme(fig: go.Figure, config: BoxConfig) -> go.Figure:
    """
    Applies a consistent layout and theme to a Plotly box plot.

    This function handles all styling and layout adjustments, such as titles,
    dimensions, templates, and trace properties, separating these concerns
    from the initial data mapping.

    Parameters
    ----------
    fig : go.Figure
        The Plotly figure object to be styled.
    config : BoxConfig
        The configuration object containing all styling and layout info.

    Returns
    -------
    go.Figure
        The styled Plotly figure object.
    """
    # Apply trace-specific updates for box plots
    fig.update_traces(
        boxpoints=config.points, notched=config.notched, selector=dict(type="box")
    )

    # Apply common layout
    fig = _apply_common_layout(fig, config)

    return fig
