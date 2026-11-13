from pathlib import Path
from typing import Callable

import pandas as pd
import pytest
from matplotlib.figure import Figure
from pandera.errors import SchemaError
from plotly.graph_objects import Figure as PlotlyFigure

from vuecore.dimensionality_reduction import (
    get_embedding_plot_interactive,
    get_embedding_plot_static,
)
from vuecore.dimensionality_reduction.common import prepare_embedding_data

DATA_DIR = Path(__file__).parent / "data"
PLOT_FUNCTIONS = [
    (get_embedding_plot_interactive, PlotlyFigure),
    (get_embedding_plot_static, Figure),
]


@pytest.fixture
def components() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "pca_components.csv")


@pytest.fixture
def loadings() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "pca_loadings.csv", index_col=0)


@pytest.mark.parametrize("plot_func, figure_type", PLOT_FUNCTIONS)
def test_components_only(
    plot_func: Callable, figure_type: PlotlyFigure | Figure, components: pd.DataFrame
):
    assert isinstance(plot_func(components), figure_type)


@pytest.mark.parametrize("plot_func, figure_type", PLOT_FUNCTIONS)
def test_with_loadings_and_acore_args(
    plot_func: Callable,
    figure_type: PlotlyFigure | Figure,
    components: pd.DataFrame,
    loadings: pd.DataFrame,
):
    # the args dictionary returned by acore.exploratory_analysis.run_pca
    args = {"x_title": "PC1 (0.92)", "y_title": "PC2 (0.05)", "group": "group"}
    assert isinstance(plot_func(components, loadings=loadings, **args), figure_type)


@pytest.mark.parametrize("plot_func, figure_type", PLOT_FUNCTIONS)
def test_without_group(
    plot_func: Callable, figure_type: PlotlyFigure | Figure, components: pd.DataFrame
):
    figure = plot_func(components.drop(columns=["group"]), group=None)
    assert isinstance(figure, figure_type)


@pytest.mark.parametrize("plot_func, figure_type", PLOT_FUNCTIONS)
def test_unknown_group_raises(
    plot_func: Callable, figure_type: PlotlyFigure | Figure, components: pd.DataFrame
):
    with pytest.raises(ValueError, match="not found"):
        plot_func(components, group="does-not-exist")


@pytest.mark.parametrize("plot_func, figure_type", PLOT_FUNCTIONS)
def test_missing_required_columns_raises(
    plot_func: Callable,
    figure_type: PlotlyFigure | Figure,
    components: pd.DataFrame,
    loadings: pd.DataFrame,
):
    with pytest.raises(SchemaError):
        plot_func(components.drop(columns=["y"]))
    with pytest.raises(SchemaError):
        plot_func(components, loadings=loadings.drop(columns=["x"]))


@pytest.mark.parametrize("plot_func, figure_type", PLOT_FUNCTIONS)
def test_unused_kwargs_are_ignored(
    plot_func: Callable, figure_type: PlotlyFigure | Figure, components: pd.DataFrame
):
    assert isinstance(plot_func(components, not_an_argument=1), figure_type)


def test_loading_value_is_optional(components: pd.DataFrame, loadings: pd.DataFrame):
    _, selected = prepare_embedding_data(
        components, loadings.drop(columns=["value"]), top_n_loadings=2
    )
    assert set(selected.index) == set(loadings.nlargest(2, "value").index)


def test_interactive_draws_top_n_loadings(
    components: pd.DataFrame, loadings: pd.DataFrame
):
    figure = get_embedding_plot_interactive(
        components, loadings=loadings, top_n_loadings=2
    )

    assert len(figure.layout.annotations) == 2
    assert {a.text for a in figure.layout.annotations} == set(
        loadings.nlargest(2, "value").index
    )


def test_loadings_are_scaled_to_components(
    components: pd.DataFrame, loadings: pd.DataFrame
):
    _, scaled = prepare_embedding_data(components, loadings)
    max_component = components[["x", "y"]].abs().to_numpy().max()
    max_arrow = (scaled["x"] ** 2 + scaled["y"] ** 2).pow(0.5).max()
    assert max_arrow == pytest.approx(0.8 * max_component)

    _, scaled = prepare_embedding_data(components, loadings, loading_factor=2)
    pd.testing.assert_series_equal(
        scaled["x"], loadings.loc[scaled.index, "x"] * 2, check_names=False
    )


def test_legacy_get_pca_plot_warns(components: pd.DataFrame, loadings: pd.DataFrame):
    from vuecore.viz import get_pca_plot

    with pytest.warns(DeprecationWarning):
        figure = get_pca_plot(
            (components, loadings, [0.92, 0.05]), "pca", {"loadings": 3}
        )
    assert isinstance(figure, PlotlyFigure)


@pytest.fixture
def three_components(components: pd.DataFrame, loadings: pd.DataFrame):
    """PCA-like output with a third dimension, as returned by acore."""
    components = components.assign(z=components["x"] - components["y"])
    loadings = loadings.assign(z=loadings["x"] * 0.5)
    annotation = {"x": "PC1 (0.92)", "y": "PC2 (0.05)", "z": "PC3 (0.02)"}
    return components, loadings, annotation


@pytest.mark.parametrize("plot_func, figure_type", PLOT_FUNCTIONS)
def test_acore_results_are_fed_directly(
    plot_func: Callable,
    figure_type: PlotlyFigure | Figure,
    components: pd.DataFrame,
    loadings: pd.DataFrame,
):
    pca = (components, loadings, [0.92, 0.05]), {"x": "PC1 (0.92)", "y": "PC2 (0.05)"}
    assert isinstance(plot_func(*pca), figure_type)
    umap = {"umap": components}, {"x": "UMAP1", "y": "UMAP2"}
    assert isinstance(plot_func(*umap), figure_type)


def test_invalid_results_raise(components: pd.DataFrame):
    with pytest.raises(ValueError, match="results must be"):
        get_embedding_plot_interactive((components, components))


def test_annotation_names_axes(components: pd.DataFrame):
    annotation = {"x": "UMAP1", "y": "UMAP2"}
    figure = get_embedding_plot_interactive(components, annotation)
    assert figure.layout.xaxis.title.text == "UMAP1"
    assert figure.layout.yaxis.title.text == "UMAP2"
    figure = get_embedding_plot_static(components, annotation, x_title="custom")
    assert figure.axes[0].get_xlabel() == "custom"
    assert figure.axes[0].get_ylabel() == "UMAP2"


@pytest.mark.parametrize("plot_func, figure_type", PLOT_FUNCTIONS)
def test_plot_other_components(plot_func, figure_type, three_components):
    components, loadings, annotation = three_components
    figure = plot_func(
        (components, loadings, None), annotation, x="x", y="z", top_n_loadings=3
    )
    assert isinstance(figure, figure_type)
    if figure_type is PlotlyFigure:
        assert figure.layout.yaxis.title.text == "PC3 (0.02)"
        assert "z=%{customdata" not in figure.data[0].hovertemplate
    else:
        assert figure.axes[0].get_ylabel() == "PC3 (0.02)"


def test_unknown_dimension_raises(components: pd.DataFrame):
    with pytest.raises(ValueError, match="not found in components"):
        get_embedding_plot_static(components, y="z")


def test_scaling_uses_plotted_dimensions(three_components):
    components, loadings, _ = three_components
    _, scaled = prepare_embedding_data(components, loadings, x="x", y="z")
    max_component = components[["x", "z"]].abs().to_numpy().max()
    max_arrow = (scaled["x"] ** 2 + scaled["z"] ** 2).pow(0.5).max()
    assert max_arrow == pytest.approx(0.8 * max_component)
