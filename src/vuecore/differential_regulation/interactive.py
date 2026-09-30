# %%
from __future__ import annotations

from logging import getLogger

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from acore.types.differential_analysis import AnovaSchema, AnovaSchemaMultiGroup
from pandera.typing.pandas import DataFrame

from vuecore.differential_regulation.common import (
    add_comparison_column,
    assign_regulation,
    build_color_map,
    format_comparison_title,
    label_top_n,
    validate_differential_regulation,
)

logger = getLogger(__name__)

DIFFERENTIAL_HOVERING_COLS = [
    "padj",
    "FC",
    "mean(group1)",
    "mean(group2)",
    "rejected",
]


def set_legend_marker_size(figure: go.Figure, size: float = 14) -> None:
    """Show all legend entries with the same, fixed marker size.

    The legend entries are replaced by legend-only proxy traces, which leaves
    the plotted markers untouched. Proxies share the ``legendgroup`` of the
    trace they replace, so clicking an entry still toggles its group.

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
        trace.update(showlegend=False, legendgroup=legendgroup)
        proxies.append(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker={
                    "size": size,
                    "color": trace.marker.color,
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


def get_volcano_plot_plotly(
    data: pd.DataFrame,
    x: str = "log2FC",
    y: str = "-log10 pvalue",
    group: str | None = None,
    hovering_cols: list[str] | None = None,
    text: str | None = None,
    title: str = "Volcano plot",
    x_title: str = "log2 fold change",
    y_title: str = "-log10(p-value)",
    height: int = 800,
    width: int = 900,
    colors: dict[str, str] | None = None,
    legend_marker_size: float | None = 14,
) -> go.Figure:
    """
    Plot a volcano plot as a scatter plot.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame with the columns referenced by the other arguments. The index
        is shown when hovering.
    x : str, optional
        Column in `data` with the values for x, e.g. the log2 fold change.
    y : str, optional
        Column in `data` with the values for y, e.g. -log10 p-values.
    group : str, optional
        Column in `data` with the groups - translates into colors.
    hovering_cols : list[str], optional
        Columns in `data` that will be shown when hovering over a dot.
    text : str, optional
        Column in `data` with the text shown next to each dot, empty strings
        are not shown.
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
    legend_marker_size : float, optional
        Fixed marker size (in pixels) for the legend entries. Pass `None` to let
        the legend follow the plotted markers.

    Returns
    -------
    plotly.graph_objects.Figure
        The volcano plot figure.

    Examples
    --------
    >>> figure = get_volcano_plot_plotly(
    ...     data, x="log2FC", y="-log10 pvalue", group="regulation"
    ... )
    """
    figure = px.scatter(
        data,
        x=x,
        y=y,
        color=group,
        color_discrete_map=colors,
        hover_name=data.index,
        hover_data=hovering_cols,
        text=text,
    )
    figure.update_traces(
        marker={"opacity": 0.7, "line": {"width": 0.5, "color": "DarkSlateGrey"}},
        textposition="top center",
    )
    figure.update_layout(
        title=title,
        xaxis={"title": x_title},
        yaxis={"title": y_title},
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
        template="plotly_white",
    )
    if group is not None and legend_marker_size is not None:
        set_legend_marker_size(figure, legend_marker_size)
    return figure


# acore related plotting function using a defined type in acore.types
def get_differential_regulation_plot(
    data: pd.DataFrame | DataFrame[AnovaSchema] | DataFrame[AnovaSchemaMultiGroup],
    comparison: str | None = None,
    top_n: int = 20,
    width: int = 900,
    height: int = 800,
    title: str = "Volcano plot",
    colors: dict[str, str] | list[str] | None = None,
    hovering_cols: list[str] = DIFFERENTIAL_HOVERING_COLS,
    legend_marker_size: float | None = 14,
    **kwargs,
) -> go.Figure:
    """
    Create an interactive volcano plot for a single comparison.

    Parameters
    ----------
    data : pd.DataFrame or DataFrame[AnovaSchema] or DataFrame[AnovaSchemaMultiGroup]
        Differential regulation results validated against `AnovaSchema` (two
        groups) or `AnovaSchemaMultiGroup`, with the feature identifiers in the
        index. Comparisons are given by the 'group1' and 'group2' columns.
    comparison : str, optional
        Comparison to plot as 'group1~group2'. Required when more than one
        comparison is present; inferred automatically when there is only one.
    top_n : int, optional
        Number of features with the smallest p-values to label.
    width : int, optional
        Plot width.
    height : int, optional
        Plot height.
    title : str, optional
        Base title for the plot.
    colors : dict[str, str] or list[str], optional
        Color mapping by regulation label, or two colors for 'in group1' and
        'in group2'. Not regulated features are always light grey by default.
    hovering_cols : list, optional
        Hover columns shown in tooltips.
    legend_marker_size : float, optional
        Fixed marker size (in pixels) for the legend entries. Pass `None` to let
        the legend follow the plotted markers.
    **kwargs : dict
        Additional keyword arguments for API parity with the static version.

    Returns
    -------
    plotly.graph_objects.Figure
        The volcano plot for the selected comparison.

    Examples
    --------
    >>> figure = get_differential_regulation_plot(
    ...     results, comparison="WT~rapZE227Stop", top_n=10
    ... )
    """
    df = add_comparison_column(validate_differential_regulation(data))

    if kwargs:
        logger.info(
            f"Additional unused kwargs passed to get_differential_regulation_plot: "
            f"{kwargs}"
        )

    available = sorted(df["comparison"].unique())
    if comparison is None:
        if len(available) > 1:
            raise ValueError(
                "Multiple comparisons are available: "
                f"{', '.join(available)}. Pass `comparison` to select one."
            )
        comparison = available[0]
    elif comparison not in available:
        raise ValueError(
            f"Comparison '{comparison}' not found. Available comparisons: "
            f"{', '.join(available)}."
        )

    df = df.query("comparison == @comparison").copy()
    group1, group2 = df["group1"].iloc[0], df["group2"].iloc[0]
    df["regulation"] = assign_regulation(df, group1, group2)
    df["label"] = label_top_n(df, "pvalue", top_n)

    return get_volcano_plot_plotly(
        df,
        x="log2FC",
        y="-log10 pvalue",
        group="regulation",
        hovering_cols=hovering_cols,
        text="label",
        title=format_comparison_title(title, comparison),
        width=width,
        height=height,
        colors=build_color_map(group1, group2, colors),
        legend_marker_size=legend_marker_size,
    )


# %%
if __name__ == "__main__":
    # %%
    from pathlib import Path

    fname = Path(__file__).resolve().parents[3] / "tests/data/differential_analysis.csv"
    results = pd.read_csv(fname, index_col=0)

    figure = get_differential_regulation_plot(results, comparison="WT~rapZE227Stop")
    figure.show()
    figure = get_differential_regulation_plot(results, comparison="QC~rapZE227Stop")
    figure.show()

# %%
