import plotly.graph_objects as go

from vuecore.schemas.basic.scatter import ScatterConfig


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

    # Use the labels dictionary to set axis titles, falling back to defaults
    x_title = config.x_title or (
        config.labels.get(config.x) if config.labels else None or config.x.title()
    )
    y_title = config.y_title or (
        config.labels.get(config.y) if config.labels else None or config.y.title()
    )

    # Apply layout updates
    fig.update_layout(
        title_text=config.title,
        title_subtitle_text=config.subtitle,
        xaxis_title=x_title,
        yaxis_title=y_title,
        height=config.height,
        width=config.width,
        template=config.template,
        xaxis_type="log" if config.log_x else "linear",
        yaxis_type="log" if config.log_y else "linear",
        xaxis_range=config.range_x,
        yaxis_range=config.range_y,
        # legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="closest",
    )
    return fig
