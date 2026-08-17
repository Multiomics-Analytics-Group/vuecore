from pathlib import Path

import pandas as pd
import pytest
from matplotlib.figure import Figure
from pandera.errors import SchemaError
from plotly.graph_objects import Figure as PlotlyFigure

from vuecore.enrichment_analysis import (
    get_enrichment_plot_interactive,
    get_enrichment_plot_static,
)


@pytest.fixture
def enrichment_df() -> pd.DataFrame:
    data_path = Path(__file__).parent / "data" / "enrichment_analysis.csv"
    return pd.read_csv(data_path, index_col=0)


def test_get_enrichment_plot_infers_single_comparison(
    enrichment_df: pd.DataFrame,
):
    figure = get_enrichment_plot_interactive(enrichment_results=enrichment_df)

    assert isinstance(figure, PlotlyFigure)


def test_get_enrichment_plot_splits_by_comparison_column(
    enrichment_df: pd.DataFrame,
):
    other_df = enrichment_df.copy()
    other_df["comparison"] = "control~20 µm sulforaphane"
    combined = pd.concat([enrichment_df, other_df], ignore_index=True)

    with pytest.raises(ValueError, match="Multiple comparisons are available"):
        get_enrichment_plot_interactive(enrichment_results=combined)

    figure = get_enrichment_plot_interactive(
        enrichment_results=combined, comparison="control~20 µm sulforaphane"
    )
    assert isinstance(figure, PlotlyFigure)


def test_get_enrichment_plot_unknown_comparison_raises(
    enrichment_df: pd.DataFrame,
):
    with pytest.raises(ValueError, match="not found"):
        get_enrichment_plot_interactive(
            enrichment_results=enrichment_df, comparison="does-not-exist"
        )


def test_get_enrichment_plot_missing_required_columns_raises(
    enrichment_df: pd.DataFrame,
):
    bad_df = enrichment_df.drop(columns=["padj"])

    with pytest.raises(SchemaError):
        get_enrichment_plot_interactive(enrichment_results=bad_df)


def test_get_enrichment_plots_static_infers_single_comparison(
    enrichment_df: pd.DataFrame,
):
    figure = get_enrichment_plot_static(enrichment_results=enrichment_df)

    assert isinstance(figure, Figure)


def test_get_enrichment_plots_static_splits_by_comparison_column(
    enrichment_df: pd.DataFrame,
):
    other_df = enrichment_df.copy()
    other_df["comparison"] = "control~20 µm sulforaphane"
    combined = pd.concat([enrichment_df, other_df], ignore_index=True)

    with pytest.raises(ValueError, match="Multiple comparisons are available"):
        get_enrichment_plot_static(enrichment_results=combined)

    figure = get_enrichment_plot_static(
        enrichment_results=combined, comparison="control~20 µm sulforaphane"
    )
    assert isinstance(figure, Figure)


def test_get_enrichment_plots_static_unknown_comparison_raises(
    enrichment_df: pd.DataFrame,
):
    with pytest.raises(ValueError, match="not found"):
        get_enrichment_plot_static(
            enrichment_results=enrichment_df, comparison="does-not-exist"
        )
