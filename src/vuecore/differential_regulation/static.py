# %%
from __future__ import annotations

from logging import getLogger

import matplotlib.axes
import matplotlib.figure
import matplotlib.pyplot as plt
import pandas as pd
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

DEFAULT_DPI = 100

logger = getLogger(__name__)


def set_legend_marker_size(ax: matplotlib.axes.Axes, size: float = 14) -> None:
    """Pin the markers of the axes' legend to a fixed size.

    Call this on any legend you (re-)create, as ``ax.legend`` discards sizes set
    before. Without a legend, nothing happens.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes whose current legend should be updated.
    size : float, optional
        Marker size as a diameter in points, as in ``Line2D.markersize``.
    """
    legend = ax.get_legend()
    if legend is None:
        return
    for handle in legend.legend_handles:
        # `s` of `Axes.scatter` is an area in points squared
        handle.set_sizes([size**2])


def get_volcano_plot_mpl(
    data: pd.DataFrame,
    x: str = "log2FC",
    y: str = "-log10 pvalue",
    group: str | None = None,
    text: str | None = None,
    title: str = "Volcano plot",
    x_title: str = "log2 fold change",
    y_title: str = "-log10(p-value)",
    height: int = 500,
    width: int = 700,
    colors: dict[str, str] | None = None,
    legend_marker_size: float | None = 10,
) -> matplotlib.figure.Figure:
    """
    Plot a volcano plot as a matplotlib scatter plot.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame with the columns referenced by the other arguments.
    x : str, optional
        Column in `data` with the values for x, e.g. the log2 fold change.
    y : str, optional
        Column in `data` with the values for y, e.g. -log10 p-values.
    group : str, optional
        Column in `data` with the groups - translates into colors and legend
        entries. Without it, all points share one color and there is no legend.
    text : str, optional
        Column in `data` with the text shown next to each dot, empty strings are
        not shown.
    title : str, optional
        Title of the figure.
    x_title : str, optional
        Plot x axis title.
    y_title : str, optional
        Plot y axis title.
    height : int, optional
        Plot height in pixels at 100 DPI.
    width : int, optional
        Plot width in pixels at 100 DPI.
    colors : dict[str, str], optional
        Mapping of group name to color. Missing groups fall back to blue.
    legend_marker_size : float, optional
        Fixed marker size for the legend entries, given as a diameter in points.
        Pass `None` to keep the plotted marker sizes.

    Returns
    -------
    matplotlib.figure.Figure
        The volcano plot figure.

    Examples
    --------
    >>> figure = get_volcano_plot_mpl(
    ...     data, x="log2FC", y="-log10 pvalue", group="regulation"
    ... )
    """
    colors = colors or {}
    fig, ax = plt.subplots(
        figsize=(width / DEFAULT_DPI, height / DEFAULT_DPI), dpi=DEFAULT_DPI
    )
    scatter_kwargs = {"alpha": 0.7, "linewidths": 0.5, "edgecolors": "DarkSlateGrey"}
    if group is None:
        ax.scatter(data[x], data[y], color="#4c78a8", **scatter_kwargs)
    else:
        for group_value, part in data.groupby(group, sort=False, observed=True):
            ax.scatter(
                part[x],
                part[y],
                color=colors.get(group_value, "#4c78a8"),
                label=group_value,
                **scatter_kwargs,
            )
        ax.legend(loc="best", frameon=False)
        if legend_marker_size is not None:
            set_legend_marker_size(ax, legend_marker_size)
    if text is not None:
        for x_value, y_value, label in zip(data[x], data[y], data[text]):
            if label:
                ax.annotate(
                    label,
                    (x_value, y_value),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha="center",
                    fontsize=7,
                )
    ax.set_xlabel(x_title)
    ax.set_ylabel(y_title)
    ax.set_title(title)
    ax.grid(linestyle="--", linewidth=0.5, alpha=0.4)
    ax.set_axisbelow(True)
    fig.tight_layout()
    return fig


# acore related plotting function using a defined type in acore.types
def get_differential_regulation_plot(
    data: pd.DataFrame | DataFrame[AnovaSchema] | DataFrame[AnovaSchemaMultiGroup],
    comparison: str | None = None,
    top_n: int = 20,
    width: int = 700,
    height: int = 500,
    title: str = "Volcano plot",
    colors: dict[str, str] | list[str] | None = None,
    legend_marker_size: float | None = 10,
    **kwargs,
) -> matplotlib.figure.Figure:
    """
    Create a static volcano plot for a single comparison using matplotlib.

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
        Plot width in pixels at 100 DPI.
    height : int, optional
        Plot height in pixels at 100 DPI.
    title : str, optional
        Base title for the plot.
    colors : dict[str, str] or list[str], optional
        Color mapping by regulation label, or two colors for 'upregulated in group1' and
        'upregulated in group2'. Not regulated features are always light grey by default.
    legend_marker_size : float, optional
        Fixed marker size for the legend entries, given as a diameter in points.
    **kwargs : dict
        Additional keyword arguments for API parity with the interactive
        version. Static figures do not render hover tooltips.

    Returns
    -------
    matplotlib.figure.Figure
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

    return get_volcano_plot_mpl(
        df,
        x="log2FC",
        y="-log10 pvalue",
        group="regulation",
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
    figure = get_differential_regulation_plot(
        results, comparison="QC~rapZE227Stop", legend_marker_size=8
    )

# %%
