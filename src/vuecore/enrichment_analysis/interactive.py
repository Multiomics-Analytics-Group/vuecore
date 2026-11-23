# %%
from __future__ import annotations

from logging import getLogger

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from acore.types.enrichment_analysis import EnrichmentAnalysisSchema
from pandera.typing.pandas import DataFrame

from vuecore.enrichment_analysis.common import (
    ODDS_RATIO_LABEL,
    PVALUE_LABEL,
    format_comparison_title,
    prepare_enrichment_data,
    select_comparison,
)

logger = getLogger(__name__)

ENRICHMENT_HOVERING_COLS = [
    "odds_ratio",
    "odds_ratio_lower",
    "foreground",
    "foreground_pop",
    "background",
    "background_pop",
    "pvalue",
    "padj",
    "identifiers",
]


def set_legend_marker_size(figure: go.Figure, size: float = 14) -> None:
    """Show all legend entries with the same, fixed marker size.

    Plotly derives the legend symbols from the trace markers, so scaling the
    markers by a column (``size``) makes the legend entries differ in size. The
    legend entries are therefore replaced by legend-only proxy traces, which
    leaves the plotted markers untouched. Proxies share the ``legendgroup`` of
    the trace they replace, so clicking an entry still toggles its group.

    Parameters
    ----------
    figure : plotly.graph_objects.Figure
        Figure to update in place.
    size : float, optional
        Marker size in pixels, as in ``marker.size``.
    """
    proxies = []
    for trace in figure.data:
        if trace.showlegend is False or not trace.name:
            continue
        legendgroup = trace.legendgroup or trace.name
        color = trace.marker.color
        if color is not None and not isinstance(color, str):
            color = "lightgrey"  # data-driven colors (color bar) have no legend color
        trace.update(showlegend=False, legendgroup=legendgroup)
        proxies.append(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker={
                    "size": size,
                    "color": color,
                    "symbol": trace.marker.symbol,
                    "opacity": trace.marker.opacity,
                    "line": trace.marker.line,
                },
                name=trace.name,
                legendgroup=legendgroup,
                showlegend=True,
                hoverinfo="skip",
            )
        )
    figure.add_traces(proxies)


def get_enrichment_plot_plotly(
    data: pd.DataFrame,
    x: str = "x",
    y: str = "y",
    group: str | None = None,
    hovering_cols: list[str] | None = None,
    size: str | None = None,
    symbol: str | None = None,
    trendline: str | None = None,
    text: str | None = None,
    title: str = "Scatter plot",
    x_title: str = "x",
    y_title: str = "y",
    height: int = 800,
    width: int = 800,
    colors: dict[str, str] | None = None,
    color_continuous: str | None = None,
    color_continuous_scale: str | None = None,
    color_title: str | None = None,
    log_x: bool = False,
    legend_marker_size: float | None = 14,
) -> go.Figure:
    """
    Plot a simple scatter plot.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame with the columns referenced by the other arguments, at least the
        x and y values to plot.
    x : str, optional
        Column in `data` with the values for x.
    y : str, optional
        Column in `data` with the values for y.
    group : str, optional
        Column in `data` with the groups - translates into colors.
    hovering_cols : list[str], optional
        Columns in `data` that will be shown when hovering over a dot.
    size : str, optional
        Column in `data` that contains the size of the dots.
    symbol : str, optional
        Column in `data` that contains the symbol of the dots.
    trendline : str, optional
        Trendline to draw, as in `plotly.express.scatter` (e.g. 'ols').
    text : str, optional
        Column in `data` that contains the values shown for each dot.
    title : str, optional
        Title of the figure.
    x_title : str, optional
        Plot x axis title.
    y_title : str, optional
        Plot y axis title.
    height : int, optional
        Plot height.
    width : int, optional
        Plot width.
    colors : dict[str, str], optional
        Mapping of group name to color, used for each group.
    color_continuous : str, optional
        Column in `data` with numeric values mapped to a color bar. Takes
        precedence over `group` for the color; `group` can still set `symbol`.
    color_continuous_scale : str, optional
        Name of the plotly color scale used for `color_continuous`.
    color_title : str, optional
        Title of the color bar.
    log_x : bool, optional
        Use a log10 scale for the x-axis.
    legend_marker_size : float, optional
        Fixed marker size (in pixels) for the legend entries, independent of the
        marker sizes in the plot. Pass `None` to let the legend follow the plotted
        marker sizes.

    Returns
    -------
    plotly.graph_objects.Figure
        The scatter plot figure.

    Examples
    --------
    >>> result = get_enrichment_plot_plotly(
    ...     data,
    ...     title="Scatter Plot",
    ...     x_title="x_axis",
    ...     y_title="y_axis",
    ...     height=100,
    ...     width=100,
    ... )
    """
    figure = px.scatter(
        data,
        x=x,
        y=y,
        color=color_continuous or group,
        color_discrete_map=None if color_continuous else colors,
        color_continuous_scale=color_continuous_scale,
        hover_data=hovering_cols,
        size=size,
        symbol=symbol,
        trendline=trendline,
        text=text,
    )

    figure.update_traces(
        marker={
            "opacity": 0.7,
            "line": {"width": 0.5, "color": "DarkSlateGrey"},
        },
        selector={"mode": "markers"},
    )
    figure["layout"] = go.Layout(
        title=title,
        xaxis={"title": x_title, "type": "log" if log_x else "linear"},
        # first row on top, as in the static plot
        yaxis={"title": y_title, "autorange": "reversed"},
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.0,
            "xanchor": "right",
            "x": 1,
        },
        hovermode="closest",
        height=height,
        width=width,
        annotations=[
            {"xref": "paper", "yref": "paper", "showarrow": False, "text": ""}
        ],
        template="plotly_white",
        coloraxis=(
            {
                "colorbar": {"title": color_title},
                "colorscale": color_continuous_scale,
            }
            if color_continuous
            else None
        ),
    )
    if log_x:
        figure.add_vline(x=1, line={"color": "grey", "dash": "dot", "width": 1})

    if group is not None and legend_marker_size is not None:
        set_legend_marker_size(figure, legend_marker_size)

    return figure


# acore related plotting function using a defined type in acore.types
# ToDo: move to acore.plotting?
def get_enrichment_plot(
    enrichment_results: pd.DataFrame | DataFrame[EnrichmentAnalysisSchema],
    comparison: str | None = None,
    width: int = 900,
    height: int = 800,
    title: str = "Enrichment",
    x: str | None = None,
    color_continuous_scale: str = "Viridis_r",
    hovering_cols: list = ENRICHMENT_HOVERING_COLS,
    legend_marker_size: float | None = 14,
    **kwargs,
) -> go.Figure:
    """
    Create an interactive enrichment scatter plot for a single comparison.

    Parameters
    ----------
    enrichment_results : Union[pd.DataFrame, DataFrame[EnrichmentAnalysisSchema]]
        Enrichment results validated against `EnrichmentAnalysisSchema`, with
        one or more comparisons stacked in the 'comparison' column.
    comparison : str, optional
        Comparison to plot. Required when more than one comparison is present;
        inferred automatically when there is only one.
    width : int, optional
        Plot width.
    height : int, optional
        Plot height.
    title : str, optional
        Base title for the plot.
    x : {'odds_ratio_lower', 'padj'}, optional
        Value on the x-axis. 'odds_ratio_lower' shows the lower bound of the
        odds ratio on a log10 scale and ranks the terms by it (rows with a
        missing or zero lower bound are dropped with a warning). 'padj' shows
        -log10(padj). By default 'odds_ratio_lower' is used if available.
    color_continuous_scale : str, optional
        Plotly color scale name for the color bar of -log10(padj).
    hovering_cols : list, optional
        Hover columns shown in tooltips.
    legend_marker_size : float, optional
        Fixed marker size (in pixels) for the legend entries, independent of the
        marker sizes in the plot. Pass `None` to let the legend follow the
        plotted marker sizes.
    **kwargs : dict
        Additional keyword arguments for API parity with the static version.

    Returns
    -------
    plotly.graph_objects.Figure
        The scatter plot for the selected comparison.
    """
    df: pd.DataFrame = EnrichmentAnalysisSchema.validate(enrichment_results)

    if kwargs:
        logger.info(f"Additional unused kwargs passed to get_enrichment_plot: {kwargs}")

    comparison = select_comparison(df, comparison)
    df, x = prepare_enrichment_data(df, comparison, x=x)
    use_odds_ratio = x == "odds_ratio_lower"

    return get_enrichment_plot_plotly(
        df,
        x="x",
        y="terms",
        group="direction",
        symbol="direction",
        size="foreground",  # column foreground in enrichment_result
        hovering_cols=hovering_cols,
        color_continuous="neg_log10_padj",
        color_continuous_scale=color_continuous_scale,
        color_title=PVALUE_LABEL,
        log_x=use_odds_ratio,
        title=format_comparison_title(title, comparison),
        x_title=ODDS_RATIO_LABEL if use_odds_ratio else PVALUE_LABEL,
        y_title="Enriched terms",
        width=width,
        height=height,
        legend_marker_size=legend_marker_size,
    )


# %%
if __name__ == "__main__":
    # %%
    import pandas as pd

    fname = "/Users/heweb/Documents/repos/vuecore/tests/data/enrichment_analysis.csv"
    enrichment_results = pd.read_csv(fname, index_col=0)

    figure = get_enrichment_plot(
        enrichment_results, width=1500, height=800, title="Enrichment"
    )
    figure.show()

# %%
