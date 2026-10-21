# %%
from __future__ import annotations

from logging import getLogger

import matplotlib.axes
import matplotlib.figure
import matplotlib.pyplot as plt
import pandas as pd
from acore.types.exploratory_analysis import TwoComponentSchema, TwoLoadingsSchema
from pandera.typing.pandas import DataFrame

from vuecore.dimensionality_reduction.common import (
    DEFAULT_LOADING_COLOR,
    build_color_map,
    prepare_embedding_data,
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


def add_loadings_mpl(
    ax: matplotlib.axes.Axes,
    loadings: pd.DataFrame,
    x: str = "x",
    y: str = "y",
    color: str = DEFAULT_LOADING_COLOR,
) -> None:
    """Draw loadings as arrows from the origin, labelled by the index.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes to draw on.
    loadings : pd.DataFrame
        Loadings in the plot's coordinates, one row per feature. The index is
        used as label.
    x, y : str, optional
        Columns in `loadings` with the arrow end points.
    color : str, optional
        Color of the arrows and labels.
    """
    for feature, row in loadings.iterrows():
        ax.annotate(
            "",
            xy=(row[x], row[y]),
            xytext=(0, 0),
            arrowprops={"arrowstyle": "->", "color": color, "linewidth": 1},
        )
        ax.text(
            row[x] * 1.15,
            row[y] * 1.15,
            str(feature),
            color=color,
            ha="center",
            va="center",
            fontsize=8,
        )
    # annotations and texts do not extend the axes limits on their own
    ax.update_datalim(loadings[[x, y]].to_numpy() * 1.15)
    ax.autoscale_view()


def get_embedding_plot_mpl(
    data: pd.DataFrame,
    x: str = "x",
    y: str = "y",
    group: str | None = None,
    loadings: pd.DataFrame | None = None,
    title: str = "Embedding",
    x_title: str = "C1",
    y_title: str = "C2",
    height: int = 500,
    width: int = 600,
    colors: dict[str, str] | None = None,
    legend_marker_size: float | None = 10,
) -> matplotlib.figure.Figure:
    """
    Plot samples in two dimensions as a matplotlib scatter plot.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame with the columns referenced by the other arguments, one row
        per sample.
    x : str, optional
        Column in `data` with the values of the first dimension.
    y : str, optional
        Column in `data` with the values of the second dimension.
    group : str, optional
        Column in `data` with the groups - translates into colors and legend
        entries. Without it, all points share one color and there is no legend.
    loadings : pd.DataFrame, optional
        Loadings drawn as arrows from the origin, already scaled to the
        coordinates of `data`. Needs the columns `x` and `y`; the index is used
        as label.
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
        The embedding plot figure.

    Examples
    --------
    >>> figure = get_embedding_plot_mpl(components, group="group")
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
    if loadings is not None:
        add_loadings_mpl(ax, loadings, x=x, y=y)
    ax.set_xlabel(x_title)
    ax.set_ylabel(y_title)
    ax.set_title(title)
    ax.grid(linestyle="--", linewidth=0.5, alpha=0.4)
    ax.set_axisbelow(True)
    fig.tight_layout()
    return fig


# acore related plotting function using a defined type in acore.types
def get_embedding_plot(
    components: pd.DataFrame | DataFrame[TwoComponentSchema],
    loadings: pd.DataFrame | DataFrame[TwoLoadingsSchema] | None = None,
    group: str | None = "group",
    top_n_loadings: int = 15,
    loading_factor: float | None = None,
    title: str = "Embedding",
    x_title: str = "C1",
    y_title: str = "C2",
    width: int = 600,
    height: int = 500,
    colors: dict[str, str] | list[str] | None = None,
    legend_marker_size: float | None = 10,
    **kwargs,
) -> matplotlib.figure.Figure:
    """
    Create a static 2D plot of a dimensionality reduction using matplotlib.

    Works for PCA, t-SNE and UMAP results of `acore.exploratory_analysis`. For PCA,
    the loadings of the features can be added as arrows (a biplot).

    Parameters
    ----------
    components : DataFrame[TwoComponentSchema]
        Sample coordinates in the columns 'x' and 'y', and the groups in `group`.
    loadings : DataFrame[TwoLoadingsSchema], optional
        Feature loadings in the columns 'x' and 'y' with the feature names in the
        index and the loading strength in 'value'. Only meaningful for PCA.
    group : str, optional
        Column in `components` used to color the samples. Pass `None` to plot all
        samples in one color.
    top_n_loadings : int, optional
        Number of features with the highest loading 'value' to draw.
    loading_factor : float, optional
        Factor the loadings are multiplied with. If omitted, it is chosen so that
        the longest arrow reaches 80% of the components' range.
    title : str, optional
        Title of the figure.
    x_title : str, optional
        Plot x axis title, e.g. 'PC1 (0.92)' as returned by acore.
    y_title : str, optional
        Plot y axis title, e.g. 'PC2 (0.05)' as returned by acore.
    width : int, optional
        Plot width in pixels at 100 DPI.
    height : int, optional
        Plot height in pixels at 100 DPI.
    colors : dict[str, str] or list[str], optional
        Color mapping by group, or a list of colors assigned to the sorted groups.
    legend_marker_size : float, optional
        Fixed marker size for the legend entries, given as a diameter in points.
    **kwargs : dict
        Additional keyword arguments for API parity with the interactive
        version, e.g. `hovering_cols`. Static figures do not render hover
        tooltips.

    Returns
    -------
    matplotlib.figure.Figure
        The embedding plot.

    Examples
    --------
    >>> from acore.exploratory_analysis import run_pca
    >>> (components, loadings, _variance), args = run_pca(data, group="group")
    >>> figure = get_embedding_plot(components, loadings, **args)
    """
    if kwargs:
        logger.info(f"Additional unused kwargs passed to get_embedding_plot: {kwargs}")

    df, loadings = prepare_embedding_data(
        components,
        loadings,
        group=group,
        top_n_loadings=top_n_loadings,
        loading_factor=loading_factor,
    )

    return get_embedding_plot_mpl(
        df,
        x="x",
        y="y",
        group=group,
        loadings=loadings,
        title=title,
        x_title=x_title,
        y_title=y_title,
        width=width,
        height=height,
        colors=build_color_map(df[group], colors) if group is not None else None,
        legend_marker_size=legend_marker_size,
    )


# %%
if __name__ == "__main__":
    # %%
    from pathlib import Path

    data_dir = Path(__file__).resolve().parents[3] / "tests/data"
    components = pd.read_csv(data_dir / "pca_components.csv")
    loadings = pd.read_csv(data_dir / "pca_loadings.csv", index_col=0)

    figure = get_embedding_plot(components, x_title="PC1", y_title="PC2")
    figure = get_embedding_plot(
        components, loadings, title="PCA", x_title="PC1", y_title="PC2"
    )

# %%
