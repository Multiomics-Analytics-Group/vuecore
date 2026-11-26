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


def test_enrichment_plot_default_uses_odds_ratio_lower_on_log_axis(
    enrichment_df: pd.DataFrame,
):
    plotly_fig = get_enrichment_plot_interactive(enrichment_results=enrichment_df)
    assert plotly_fig.layout.xaxis.type == "log"
    assert "odds ratio" in plotly_fig.layout.xaxis.title.text.lower()
    assert plotly_fig.layout.coloraxis.colorbar.title.text == "-log10(padj)"

    mpl_fig = get_enrichment_plot_static(enrichment_results=enrichment_df)
    ax = mpl_fig.axes[0]
    assert ax.get_xscale() == "log"
    assert len(mpl_fig.axes) == 2  # scatter axes and color bar


def test_enrichment_plot_x_padj_uses_linear_axis(enrichment_df: pd.DataFrame):
    plotly_fig = get_enrichment_plot_interactive(
        enrichment_results=enrichment_df, x="padj"
    )
    assert plotly_fig.layout.xaxis.type == "linear"
    assert plotly_fig.layout.xaxis.title.text == "-log10(padj)"

    mpl_fig = get_enrichment_plot_static(enrichment_results=enrichment_df, x="padj")
    assert mpl_fig.axes[0].get_xscale() == "linear"


def test_enrichment_plot_invalid_x_raises(enrichment_df: pd.DataFrame):
    with pytest.raises(ValueError, match="`x` must be"):
        get_enrichment_plot_static(enrichment_results=enrichment_df, x="foo")


def test_enrichment_plot_drops_zero_and_null_lower_bounds(
    enrichment_df: pd.DataFrame, caplog: pytest.LogCaptureFixture
):
    df = enrichment_df.copy()
    n_rejected = int(df["rejected"].sum())
    df.iloc[0, df.columns.get_loc("odds_ratio_lower")] = 0.0
    df.iloc[1, df.columns.get_loc("odds_ratio_lower")] = float("nan")

    with caplog.at_level("WARNING"):
        figure = get_enrichment_plot_static(enrichment_results=df, x="odds_ratio_lower")

    assert "Dropping 2 term(s)" in caplog.text
    assert len(figure.axes[0].get_yticks()) == n_rejected - 2


def test_enrichment_plot_falls_back_to_padj_without_lower_bounds(
    enrichment_df: pd.DataFrame,
):
    df = enrichment_df.copy()
    df["odds_ratio_lower"] = float("nan")

    figure = get_enrichment_plot_interactive(enrichment_results=df)

    assert figure.layout.xaxis.type == "linear"
