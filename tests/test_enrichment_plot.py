from pathlib import Path

import pandas as pd
import pytest
from matplotlib.figure import Figure

from vuecore.enrichment_analysis import (
    create_enrichment_plots_interactive,
    get_enrichment_plots_static,
)


@pytest.fixture
def enrichment_df() -> pd.DataFrame:
    data_path = Path(__file__).parent / "data" / "enrichment_analysis.csv"
    return pd.read_csv(data_path, index_col=0)


def test_create_enrichment_plots_interactive_saves_html(
    enrichment_df: pd.DataFrame, tmp_path: Path
):
    comparison_key = "control~10 µm sulforaphane"
    result = create_enrichment_plots_interactive(
        enrichment_results={comparison_key: enrichment_df},
        output_folder=str(tmp_path),
        output_format="html",
    )

    assert comparison_key in result
    output_path = result[comparison_key]["output_path"]
    assert output_path is not None
    assert Path(output_path).exists()
    assert Path(output_path).suffix == ".html"
    assert Path(output_path).stat().st_size > 0


def test_get_enrichment_plots_static_infers_single_comparison(
    enrichment_df: pd.DataFrame,
):
    figure = get_enrichment_plots_static(enrichment_results=enrichment_df)

    assert isinstance(figure, Figure)


def test_get_enrichment_plots_static_splits_by_comparison_column(
    enrichment_df: pd.DataFrame,
):
    other_df = enrichment_df.copy()
    other_df["comparison"] = "control~20 µm sulforaphane"
    combined = pd.concat([enrichment_df, other_df], ignore_index=True)

    with pytest.raises(ValueError, match="Multiple comparisons are available"):
        get_enrichment_plots_static(enrichment_results=combined)

    figure = get_enrichment_plots_static(
        enrichment_results=combined, comparison="control~20 µm sulforaphane"
    )
    assert isinstance(figure, Figure)


def test_get_enrichment_plots_static_unknown_comparison_raises(
    enrichment_df: pd.DataFrame,
):
    with pytest.raises(ValueError, match="not found"):
        get_enrichment_plots_static(
            enrichment_results=enrichment_df, comparison="does-not-exist"
        )


def test_create_enrichment_plots_default_key_for_dataframe(
    enrichment_df: pd.DataFrame,
):
    result = create_enrichment_plots_interactive(enrichment_results=enrichment_df)

    assert "regulated~non-regulated" in result
    assert result["regulated~non-regulated"]["figure"] is not None


def test_create_enrichment_plots_missing_required_columns_raises(
    enrichment_df: pd.DataFrame,
):
    bad_df = enrichment_df.drop(columns=["padj"])

    with pytest.raises(ValueError, match="Missing required columns"):
        create_enrichment_plots_interactive(
            enrichment_results={"control~10 µm sulforaphane": bad_df}
        )


def test_create_enrichment_plots_interactive_rejects_static_format(
    enrichment_df: pd.DataFrame,
):
    with pytest.raises(ValueError, match="Unsupported output_format"):
        create_enrichment_plots_interactive(
            enrichment_results={"control~10 µm sulforaphane": enrichment_df},
            output_format="png",
        )
