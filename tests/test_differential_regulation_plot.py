from pathlib import Path
from typing import Callable

import pandas as pd
import pytest
from matplotlib.figure import Figure
from pandera.errors import SchemaError
from plotly.graph_objects import Figure as PlotlyFigure

from vuecore.differential_regulation import (
    get_differential_regulation_plot_interactive,
    get_differential_regulation_plot_static,
)

COMPARISON = "WT~rapZE227Stop"
PLOT_FUNCTIONS = [
    (get_differential_regulation_plot_interactive, PlotlyFigure),
    (get_differential_regulation_plot_static, Figure),
]


@pytest.fixture
def diff_df() -> pd.DataFrame:
    data_path = Path(__file__).parent / "data" / "differential_analysis.csv"
    return pd.read_csv(data_path, index_col=0)


@pytest.fixture
def single_df(diff_df: pd.DataFrame) -> pd.DataFrame:
    return diff_df.query("group1 == 'WT' and group2 == 'rapZE227Stop'")


@pytest.mark.parametrize("plot_func, figure_type", PLOT_FUNCTIONS)
def test_infers_single_comparison(
    plot_func: Callable, figure_type: PlotlyFigure | Figure, single_df: pd.DataFrame
):
    assert isinstance(plot_func(single_df), figure_type)


@pytest.mark.parametrize("plot_func, figure_type", PLOT_FUNCTIONS)
def test_multiple_comparisons_require_selection(
    plot_func: Callable, figure_type: PlotlyFigure | Figure, diff_df: pd.DataFrame
):
    with pytest.raises(ValueError, match="Multiple comparisons are available"):
        plot_func(diff_df)

    assert isinstance(plot_func(diff_df, comparison=COMPARISON), figure_type)


@pytest.mark.parametrize("plot_func, figure_type", PLOT_FUNCTIONS)
def test_unknown_comparison_raises(
    plot_func: Callable, figure_type: PlotlyFigure | Figure, diff_df: pd.DataFrame
):
    with pytest.raises(ValueError, match="not found"):
        plot_func(diff_df, comparison="does-not-exist")


@pytest.mark.parametrize("plot_func, figure_type", PLOT_FUNCTIONS)
def test_missing_required_columns_raises(
    plot_func: Callable, figure_type: PlotlyFigure | Figure, diff_df: pd.DataFrame
):
    with pytest.raises(SchemaError):
        plot_func(diff_df.drop(columns=["padj"]), comparison=COMPARISON)
