import pandas as pd
import pytest
from vuecore.plots.basic.scatter import create_scatter_plot


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "gene_expression": [1.2, 2.5, 3.1, 4.5, 5.2, 6.8, 3.9, 2.1],
            "log_p_value": [0.5, 1.5, 2.0, 3.5, 4.0, 5.5, 1.8, 0.9],
            "regulation": ["Up", "Up", "None", "Down", "Down", "Down", "None", "Up"],
            "significance_score": [10, 20, 5, 40, 55, 80, 15, 25],
            "gene_name": [
                "GENE_A",
                "GENE_B",
                "GENE_C",
                "GENE_D",
                "GENE_E",
                "GENE_F",
                "GENE_G",
                "GENE_H",
            ],
            "cell_type": ["A", "B", "A", "B", "A", "B", "A", "B"],
        }
    )


@pytest.mark.parametrize("ext", ["png", "svg", "pdf", "html", "json"])
def test_basic_scatter_plot(sample_df, tmp_path, ext):
    """Test basic scatter plot creation and file output for multiple formats."""
    output_path = tmp_path / f"scatter_test.{ext}"

    fig = create_scatter_plot(
        data=sample_df,
        x="gene_expression",
        y="log_p_value",
        file_path=str(output_path),
    )

    assert fig is not None
    assert output_path.exists()
    assert output_path.stat().st_size > 0


@pytest.mark.parametrize("ext", ["png", "svg", "pdf", "html", "json"])
def test_advanced_scatter_plot(sample_df, tmp_path, ext):
    """Test advanced scatter plot creation with multiple parameters and file output."""
    output_path = tmp_path / f"scatter_test.{ext}"

    fig = create_scatter_plot(
        data=sample_df,
        x="gene_expression",
        y="log_p_value",
        color="regulation",
        size="significance_score",
        text="gene_name",
        title="Advanced Gene Expression Scatter Plot",
        subtitle="Visualizing Gene Expression with Regulation and Significance",
        x_title="Log2 Fold Change",
        y_title="-Log10(P-value)",
        color_discrete_map={"Up": "#508AA8", "Down": "#A8505E", "None": "#838383"},
        opacity=0.8,
        marker_line_width=1,
        marker_line_color="darkgray",
        width=900,
        height=600,
        file_path=output_path,
    )

    assert fig is not None
    assert output_path.exists()
    assert output_path.stat().st_size > 0
