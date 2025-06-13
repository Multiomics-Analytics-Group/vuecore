import plotly.graph_objects as go
from ....schemas.distribution.scatter import ScatterConfig


def apply_plot_theme(fig: go.Figure, config: ScatterConfig) -> go.Figure:
    """
    Applies a consistent layout and theme to a Plotly figure.

    This function separates styling from plot creation, allowing for a consistent
    look and feel across different plot types. It updates traces and layout
    properties based on the provided configuration.

    Parameters
    ----------
    fig : go.Figure
        The Plotly figure object to be styled.
    config : ScatterConfig
        The configuration object containing styling info like titles and dimensions.

    Returns
    -------
    go.Figure
        The styled Plotly figure object.
    """
    fig.update_traces(
        marker=dict(opacity=0.8, line=dict(width=0.5, color="DarkSlateGrey")),
        selector=dict(mode="markers"),
    )

    fig.update_layout(
        title_text=config.title,
        xaxis_title=config.x_title or config.x.title(),
        yaxis_title=config.y_title or config.y.title(),
        height=config.height,
        width=config.width,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="closest",
    )
    return fig
