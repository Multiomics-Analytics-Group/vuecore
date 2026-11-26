# %%
from __future__ import annotations

from logging import getLogger

import matplotlib.axes
import matplotlib.colors
import matplotlib.figure
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from acore.types.enrichment_analysis import EnrichmentAnalysisSchema
from pandera.typing.pandas import DataFrame

from vuecore.enrichment_analysis.common import (
    ODDS_RATIO_LABEL,
    PVALUE_LABEL,
    format_comparison_title,
    prepare_enrichment_data,
    select_comparison,
)

DEFAULT_DPI = 100
DIRECTION_MARKERS = ["o", "s", "^", "D", "v", "P"]

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
    col_x: str = "x",
    col_color: str = "neg_log10_padj",
    col_markersize: str = "foreground",
    x_label: str = PVALUE_LABEL,
    log_x: bool = False,
    cmap: str = "viridis_r",
    color_label: str = PVALUE_LABEL,
    legend_marker_size: float = 14,
) -> matplotlib.figure.Figure:
    """Create one enrichment scatter plot as a matplotlib figure.

    Terms are drawn top to bottom in the order of `df`, so sort the rows before
    calling. Marker areas are scaled linearly between a minimum and maximum from
    the values in `col_markersize`. Points are color coded by `col_color`, with
    a color bar, and the marker shape distinguishes the values of `group`.

    Parameters
    ----------
    df : pd.DataFrame
        Rows to plot, one per enriched term. Must contain the columns `col_x`,
        `col_color`, `col_markersize`, 'terms' (used as y tick labels) and, if
        `group` is given, the grouping column.
    comparison_key : str
        Comparison identifier of the form 'group1~group2', appended to `title`
        as 'group1 vs group2'. A key without the separator is appended as is.
    group : str, optional
        Column to assign marker shapes and legend entries by, e.g. 'direction'.
        Pass None to draw all points with the same marker and no legend.
    width : int
        Plot width in pixels at 100 DPI.
    height : int
        Plot height in pixels at 100 DPI.
    title : str
        Base title, combined with `comparison_key` into the figure title.
    col_x : str, optional
        Column with the x values.
    col_color : str, optional
        Column with the values mapped to colors, by default -log10 adjusted
        p-values.
    col_markersize : str, optional
        Column driving the marker sizes, typically the foreground counts.
        Non-numeric and missing values are treated as 0.
    x_label : str, optional
        x-axis label.
    log_x : bool, optional
        Use a log10 scale for the x-axis, e.g. for odds ratios.
    cmap : str, optional
        Matplotlib colormap name for `col_color`.
    color_label : str, optional
        Label of the color bar.
    legend_marker_size : float, optional
        Fixed marker size for the legend entries, given as a diameter in points
        (as in `Line2D.markersize`), independent of the marker sizes in the plot.

    Returns
    -------
    matplotlib.figure.Figure
        The scatter plot for the given comparison.
    """
    fig_width = width / DEFAULT_DPI
    fig_height = height / DEFAULT_DPI
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=DEFAULT_DPI)

    y_positions = np.arange(len(df))
    marker_sizes = np.asarray(_scale_marker_sizes(df[col_markersize]), dtype=float)
    x_values = df[col_x].to_numpy()
    c_values = df[col_color].to_numpy(dtype=float)
    norm = matplotlib.colors.Normalize(
        vmin=np.nanmin(c_values) if len(c_values) else 0,
        vmax=np.nanmax(c_values) if len(c_values) else 1,
    )
    scatter_kwargs = {
        "alpha": 0.8,
        "linewidths": 0.5,
        "edgecolors": "DarkSlateGrey",
        "cmap": cmap,
        "norm": norm,
    }

    if group is None:
        mappable = ax.scatter(
            x_values, y_positions, s=marker_sizes, c=c_values, **scatter_kwargs
        )
    else:
        # positional indices, so that a non-unique index cannot mislabel rows
        grouped = df.groupby(group, sort=False, observed=True)
        for i, (group_value, positions) in enumerate(grouped.indices.items()):
            mappable = ax.scatter(
                x_values[positions],
                y_positions[positions],
                s=marker_sizes[positions],
                c=c_values[positions],
                marker=DIRECTION_MARKERS[i % len(DIRECTION_MARKERS)],
                label=group_value,
                **scatter_kwargs,
            )
        ax.legend(loc="best", frameon=False)
        set_legend_marker_size(ax, legend_marker_size)
        # legend markers should not carry a data color
        legend = ax.get_legend()
        if legend is not None:
            for handle in legend.legend_handles:
                handle.set_facecolor("lightgrey")
    if len(df):
        fig.colorbar(mappable, ax=ax, label=color_label)
    if log_x:
        ax.set_xscale("log")
        low, high = ax.get_xlim()
        if low < 1 < high:  # reference for no effect
            ax.axvline(1, color="grey", linestyle=":", linewidth=1)
    ax.set_yticks(y_positions)
    ax.set_yticklabels(df["terms"])
    ax.set_xlabel(x_label)
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
    x: str | None = None,
    cmap: str = "viridis_r",
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
    x : {'odds_ratio_lower', 'padj'}, optional
        Value on the x-axis. 'odds_ratio_lower' shows the lower bound of the
        odds ratio on a log10 scale and ranks the terms by it (rows with a
        missing or zero lower bound are dropped with a warning). 'padj' shows
        -log10(padj). By default 'odds_ratio_lower' is used if available.
    cmap : str, optional
        Matplotlib colormap name for the color bar of -log10(padj).
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

    comparison = select_comparison(df, comparison)
    df, x = prepare_enrichment_data(df, comparison, x=x)
    use_odds_ratio = x == "odds_ratio_lower"

    return get_enrichment_plot_mpl(
        df=df,
        comparison_key=comparison,
        group="direction",
        width=width,
        height=height,
        title=title,
        col_x="x",
        col_color="neg_log10_padj",
        col_markersize="foreground",
        x_label=ODDS_RATIO_LABEL if use_odds_ratio else PVALUE_LABEL,
        log_x=use_odds_ratio,
        cmap=cmap,
        color_label=PVALUE_LABEL,
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
