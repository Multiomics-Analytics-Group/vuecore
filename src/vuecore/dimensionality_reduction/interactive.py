# %%
from __future__ import annotations

from logging import getLogger

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from acore.types.exploratory_analysis import (
    AnnotationResult,
    TwoComponentSchema,
    TwoLoadingsSchema,
)
from pandera.typing.pandas import DataFrame

from vuecore.dimensionality_reduction.common import (
    DEFAULT_LOADING_COLOR,
    as_column_name,
    build_color_map,
    get_axis_titles,
    prepare_embedding_data,
    unpack_results,
)

logger = getLogger(__name__)


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


def add_loadings_plotly(
    figure: go.Figure,
    loadings: pd.DataFrame,
    x: str = "x",
    y: str = "y",
    value: str | None = "value",
    color: str = DEFAULT_LOADING_COLOR,
) -> None:
    """Draw loadings as lines from the origin, labelled by the index.

    Parameters
    ----------
    figure : plotly.graph_objects.Figure
        Figure to update in place.
    loadings : pd.DataFrame
        Loadings in the plot's coordinates, one row per feature. The index is
        used as label.
    x, y : str, optional
        Columns in `loadings` with the arrow end points.
    value : str, optional
        Column in `loadings` shown when hovering over an arrow.
    color : str, optional
        Color of the lines and labels.
    """
    for feature, row in loadings.iterrows():
        hover_text = str(feature)
        if value is not None:
            hover_text += f" loading: {row[value]:.2f}"
        figure.add_trace(
            go.Scatter(
                x=[0, row[x]],
                y=[0, row[y]],
                mode="markers+lines",
                marker={"size": 3, "color": color},
                line={"color": color},
                text=hover_text,
                hoverinfo="text",
                name=str(feature),
                showlegend=False,
            )
        )
        figure.add_annotation(
            x=row[x] * 1.15,
            y=row[y] * 1.15,
            text=str(feature),
            showarrow=False,
            font={"size": 12, "color": color},
        )


def get_embedding_plot_plotly(
    data: pd.DataFrame,
    x: str = "x",
    y: str = "y",
    group: str | None = None,
    hovering_cols: list[str] | None = None,
    loadings: pd.DataFrame | None = None,
    title: str = "Embedding",
    x_title: str = "C1",
    y_title: str = "C2",
    height: int = 800,
    width: int = 800,
    colors: dict[str, str] | None = None,
    legend_marker_size: float | None = 14,
) -> go.Figure:
    """
    Plot samples in two dimensions, optionally with loadings as a biplot.

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
        Column in `data` with the groups - translates into colors.
    hovering_cols : list[str], optional
        Columns in `data` that will be shown when hovering over a dot.
    loadings : pd.DataFrame, optional
        Loadings drawn as lines from the origin, already scaled to the
        coordinates of `data`. Needs the columns `x` and `y`, and 'value' which
        is shown when hovering. The index is used as label.
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
        The embedding plot figure.

    Examples
    --------
    >>> figure = get_embedding_plot_plotly(components, group="group")
    """
    figure = px.scatter(
        data,
        x=x,
        y=y,
        color=group,
        color_discrete_map=colors,
        hover_data=hovering_cols,
    )
    figure.update_traces(
        marker={
            "size": 14,
            "opacity": 0.7,
            "line": {"width": 0.5, "color": "DarkSlateGrey"},
        },
    )
    if loadings is not None:
        add_loadings_plotly(
            figure, loadings, x=x, y=y, value="value" if "value" in loadings else None
        )
    figure.update_layout(
        title=title,
        xaxis={"title": x_title},
        yaxis={"title": y_title},
        legend={
            "title": {"text": ""},  # px would use the name of the `group` column
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
def get_embedding_plot(
    results: pd.DataFrame | DataFrame[TwoComponentSchema] | tuple | list | dict,
    annotation: AnnotationResult | dict | None = None,
    loadings: pd.DataFrame | DataFrame[TwoLoadingsSchema] | None = None,
    group: str | None = "group",
    x: str | int = "x",
    y: str | int = "y",
    top_n_loadings: int = 15,
    loading_factor: float | None = None,
    title: str = "Embedding",
    x_title: str | None = None,
    y_title: str | None = None,
    width: int = 800,
    height: int = 800,
    colors: dict[str, str] | list[str] | None = None,
    hovering_cols: list[str] | None = None,
    legend_marker_size: float | None = 14,
    **kwargs,
) -> go.Figure:
    """
    Create an interactive 2D plot of a dimensionality reduction.

    Works for PCA, t-SNE and UMAP results of `acore.exploratory_analysis`. For PCA,
    the loadings of the features can be added as arrows (a biplot).

    Parameters
    ----------
    results : DataFrame[TwoComponentSchema], tuple or dict
        The first return value of `acore.exploratory_analysis.run_pca`,
        `run_tsne` or `run_umap` as it is: the `(components, loadings, variance)`
        tuple of PCA, or the one-entry dictionary of t-SNE and UMAP. A components
        DataFrame with the sample coordinates in the columns 'x' and 'y' and the
        groups in `group` works as well.
        Additional columns, e.g. 'sample', are shown when hovering.
    annotation : AnnotationResult or dict, optional
        The second return value of the acore function. It names the axes, e.g.
        'PC1 (0.92)', unless `x_title` or `y_title` are given.
    loadings : DataFrame[TwoLoadingsSchema], optional
        Feature loadings in the columns 'x' and 'y' with the feature names in the
        index and the loading strength in 'value'. Only meaningful for PCA, where
        they are taken from `results`. Passing them here overrides those.
    group : str, optional
        Column in the components used to color the samples. Pass `None` to plot
        all samples in one color.
    x, y : str, optional
        Columns of the dimensions to plot, e.g. `y="z"` to plot the first against
        the third component. Further components are named '3', '4', ... (the
        fourth is `y=3` or `y="3"`). The loadings are ranked by their 'value' over all
        components.
    top_n_loadings : int, optional
        Number of features with the highest loading 'value' to draw.
    loading_factor : float, optional
        Factor the loadings are multiplied with. If omitted, it is chosen so that
        the longest arrow reaches 80% of the components' range.
    title : str, optional
        Title of the figure.
    x_title : str, optional
        Plot x axis title. Defaults to the name in `annotation`, then to `x`.
    y_title : str, optional
        Plot y axis title. Defaults to the name in `annotation`, then to `y`.
    width : int, optional
        Plot width.
    height : int, optional
        Plot height.
    colors : dict[str, str] or list[str], optional
        Color mapping by group, or a list of colors assigned to the sorted groups.
    hovering_cols : list[str], optional
        Columns in the components shown when hovering. Defaults to all columns
        except the plotted `x` and `y`, and `group`.
    legend_marker_size : float, optional
        Fixed marker size (in pixels) for the legend entries. Pass `None` to let
        the legend follow the plotted markers.
    **kwargs : dict
        Additional keyword arguments for API parity with the static version.

    Returns
    -------
    plotly.graph_objects.Figure
        The embedding plot.

    Examples
    --------
    >>> from acore.exploratory_analysis import run_pca, run_umap
    >>> figure = get_embedding_plot(*run_pca(data, group="group"))
    >>> figure = get_embedding_plot(*run_umap(data, group="group"))
    """
    if kwargs:
        logger.info(f"Additional unused kwargs passed to get_embedding_plot: {kwargs}")

    components, loadings = unpack_results(results, loadings)
    x, y = as_column_name(x), as_column_name(y)
    df, loadings = prepare_embedding_data(
        components,
        loadings,
        group=group,
        top_n_loadings=top_n_loadings,
        loading_factor=loading_factor,
        x=x,
        y=y,
    )
    x_title, y_title = get_axis_titles(annotation, x, y, x_title, y_title)
    if hovering_cols is None:
        hovering_cols = df.columns.difference([x, y, group]).tolist()

    return get_embedding_plot_plotly(
        df,
        x=x,
        y=y,
        group=group,
        hovering_cols=hovering_cols,
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
    figure.show()
    figure = get_embedding_plot(
        components, loadings, title="PCA", x_title="PC1", y_title="PC2"
    )
    figure.show()

# %%
