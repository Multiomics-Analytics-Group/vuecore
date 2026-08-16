# %%
from __future__ import annotations

from logging import getLogger

import matplotlib.axes
import matplotlib.figure
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from acore.types.enrichment_analysis import EnrichmentAnalysisSchema
from pandera.typing.pandas import DataFrame

from vuecore.enrichment_analysis.common import build_color_map, format_comparison_title

DEFAULT_DPI = 100

logger = getLogger(__name__)


def _scale_marker_sizes(
    values: pd.Series, min_size: float = 60.0, max_size: float = 320.0
):
    """Scale foreground counts into matplotlib marker areas."""
    numeric = pd.to_numeric(values, errors="coerce").fillna(0)
    if numeric.empty:
        return []
    min_value = float(numeric.min())
    max_value = float(numeric.max())
    if max_value <= min_value:
        return [min_size] * len(numeric)
    scaled = (numeric - min_value) / (max_value - min_value)
    return (min_size + scaled * (max_size - min_size)).tolist()


def set_legend_marker_size(ax: matplotlib.axes.Axes, size: float = 14) -> None:
    """Pin the markers of the axes' legend to a fixed size.

    Legend handles of a scatter plot inherit the data-driven marker areas, which
    makes entries differ in size. Call this on any legend you (re-)create, e.g.
    after ``ax.legend(title=...)``, as that discards the sizes set before.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes whose current legend should be updated. Without a legend, nothing
        happens.
    size : float, optional
        Marker size as a diameter in points, as in ``Line2D.markersize``.
    """
    legend = ax.get_legend()
    if legend is None:
        return
    for handle in legend.legend_handles:
        # `s` of `Axes.scatter` is an area in points squared
        handle.set_sizes([size**2])


def get_enrichment_plot_mpl(
    df: pd.DataFrame,
    comparison_key: str,
    group: str | None,
    width: int,
    height: int,
    title: str,
    colors: dict[str, str],
    col_x: str = "x",
    col_markersize: str = "foreground",
    legend_marker_size: float = 14,
) -> matplotlib.figure.Figure:
    """Create one enrichment scatter plot as a matplotlib figure.

    Terms are drawn top to bottom in the order of `df`, so sort the rows before
    calling. Marker areas are scaled linearly between a minimum and maximum from
    the values in `col_markersize`.

    Parameters
    ----------
    df : pd.DataFrame
        Rows to plot, one per enriched term. Must contain the columns `col_x`,
        `col_markersize`, 'terms' (used as y tick labels) and, if `group` is
        given, the grouping column.
    comparison_key : str
        Comparison identifier of the form 'group1~group2', appended to `title`
        as 'group1 vs group2'. A key without the separator is appended as is.
    group : str, optional
        Column to color and label the points by, e.g. 'direction'. One legend
        entry is added per unique value. Pass None to draw all points in a
        single color without a legend.
    width : int
        Plot width in pixels at 100 DPI, with a lower bound of 400.
    height : int
        Plot height in pixels at 100 DPI, with a lower bound of 300.
    title : str
        Base title, combined with `comparison_key` into the figure title.
    colors : dict[str, str]
        Color per value of the `group` column. Values missing from the mapping
        fall back to a default blue. Ignored when `group` is None.
    col_x : str, optional
        Column with the x values, expected to be -log10 transformed adjusted
        p-values.
    col_markersize : str, optional
        Column driving the marker sizes, typically the foreground counts.
        Non-numeric and missing values are treated as 0.
    legend_marker_size : float, optional
        Fixed marker size for the legend entries, given as a diameter in points
        (as in `Line2D.markersize`), independent of the marker sizes in the plot.

    Returns
    -------
    matplotlib.figure.Figure
        The scatter plot for the given comparison.
    """
    fig_width = max(width / DEFAULT_DPI, 4)
    fig_height = max(height / DEFAULT_DPI, 3)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=DEFAULT_DPI)

    y_positions = list(range(len(df)))
    marker_sizes = _scale_marker_sizes(df[col_markersize])

    if group is None:
        ax.scatter(
            df[col_x],
            y_positions,
            s=marker_sizes,
            alpha=0.7,
            linewidths=0.5,
            edgecolors="DarkSlateGrey",
            color="#4c78a8",
        )
    else:
        for group_value, group_df in df.groupby(group, sort=False):
            group_positions = [df.index.get_loc(idx) for idx in group_df.index]
            ax.scatter(
                group_df[col_x],
                group_positions,
                s=[marker_sizes[i] for i in group_positions],
                alpha=0.7,
                linewidths=0.5,
                edgecolors="DarkSlateGrey",
                color=colors.get(group_value, "#4c78a8"),
                label=group_value,
            )
        ax.legend(loc="best", frameon=False)
        set_legend_marker_size(ax, legend_marker_size)
    ax.set_yticks(y_positions)
    ax.set_yticklabels(df["terms"])
    ax.set_xlabel("-log10(padj)")
    ax.set_ylabel("Enriched terms")
    ax.set_title(format_comparison_title(title, comparison_key))
    ax.grid(axis="x", linestyle="--", linewidth=0.5, alpha=0.4)
    ax.set_axisbelow(True)
    ax.invert_yaxis()
    fig.tight_layout()
    return fig


# acore related plotting function using a defined type in acore.types
# ToDo: move to acore.plotting?
def get_enrichment_plot(
    enrichment_results: pd.DataFrame | DataFrame[EnrichmentAnalysisSchema],
    comparison: str | None = None,
    width: int = 700,
    height: int = 500,
    title: str = "Enrichment",
    colors: dict[str, str] | list[str] | None = None,
    legend_marker_size: float = 14,
    **kwargs,
) -> matplotlib.figure.Figure:
    """
    Create a static enrichment scatter plot for a single comparison based on an
    EnrichmentAnalysisSchema compliant DataFrame. The plot is rendered using matplotlib.

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
    colors : dict[str, str] or list[str], optional
        Color mapping by direction, or a palette to assign to directions in
        order. Defaults to a built-in palette, cycling if there are more
        unique directions than colors.
    legend_marker_size : float, optional
        Fixed marker size for the legend entries, given as a diameter in points
        (as in `Line2D.markersize`), independent of the marker sizes in the plot.
    **kwargs : dict
        Additional keyword arguments for API parity with the interactive version. Static figures do
        not render hover tooltips.

    Returns
    -------
    matplotlib.figure.Figure
        The scatter plot for the selected comparison.
    """

    df: pd.DataFrame = EnrichmentAnalysisSchema.validate(enrichment_results)

    if kwargs:
        logger.info(f"Additional unused kwargs passed to get_enrichment_plot: {kwargs}")

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

    df = df.query("comparison == @comparison and rejected").copy()
    df = df.sort_values(by=["direction", "padj"], ascending=False).reset_index(
        drop=True
    )
    df["x"] = -np.log10(df["padj"])
    colors = build_color_map(df["direction"], colors)

    return get_enrichment_plot_mpl(
        df=df,
        comparison_key=comparison,
        group="direction",
        width=width,
        height=height,
        title=title,
        colors=colors,
        col_x="x",
        col_markersize="foreground",
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

# %%
