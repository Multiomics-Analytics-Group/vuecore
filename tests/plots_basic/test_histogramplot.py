import pandas as pd
import numpy as np
import pytest
from pathlib import Path

from vuecore.plots.basic.histogram import create_histogram_plot


@pytest.fixture
def sample_histogram_data() -> pd.DataFrame:
    """
    Fixture for generating synthetic data for histogram plots, replicating
    the code used in the docs/api_examples/histogram_plot.ipynb example.
    """
    # Set a random seed for reproducibility of the synthetic data
    np.random.seed(42)

    # Define parameters for synthetic gene expression data
    num_genes = 1000
    gene_names = [f"Gene_{i}" for i in range(num_genes)]

    # Simulate expression data with a slight shift in the "Treated" group
    expression_values = np.concatenate(
        [
            np.random.normal(loc=10, scale=2, size=num_genes // 2),
            np.random.normal(loc=12, scale=2, size=num_genes // 2),
        ]
    )
    condition_values = np.concatenate(
        [["Control"] * (num_genes // 2), ["Treated"] * (num_genes // 2)]
    )

    # Create the DataFrame
    gene_exp_df = pd.DataFrame(
        {
            "Gene_ID": gene_names,
            "Expression": expression_values,
            "Condition": condition_values,
        }
    )
    return gene_exp_df


@pytest.mark.parametrize("ext", ["png", "svg", "html", "json"])
def test_basic_histogram_plot(
    sample_histogram_data: pd.DataFrame, tmp_path: Path, ext: str
):
    """
    Test basic histogram plot creation, ensuring the figure is returned,
    and output files are generated correctly for various formats.
    """
    # Define the output path using tmp_path fixture for temporary files
    output_path = tmp_path / f"basic_histogram_test.{ext}"

    # Create the basic histogram plot using the VueCore function
    fig = create_histogram_plot(
        data=sample_histogram_data,
        x="Expression",
        title="Distribution of Gene Expression Levels",
        file_path=str(output_path),
    )

    # Assertions to verify plot creation and file output
    assert fig is not None, "Figure object should not be None."
    assert output_path.exists(), f"Output file should exist: {output_path}"
    assert (
        output_path.stat().st_size > 0
    ), f"Output file should not be empty: {output_path}"


@pytest.mark.parametrize("ext", ["png", "svg", "html", "json"])
def test_advanced_histogram_plot(
    sample_histogram_data: pd.DataFrame, tmp_path: Path, ext: str
):
    """
    Test advanced histogram plot creation with multiple parameters,
    ensuring the figure is returned and output files are generated.
    """
    # Define the output path for the advanced plot
    output_path = tmp_path / f"advanced_histogram_test.{ext}"

    # Create the advanced histogram plot using the VueCore function
    fig = create_histogram_plot(
        data=sample_histogram_data,
        x="Expression",
        color="Condition",
        barmode="overlay",
        histnorm="probability density",
        title="Gene Expression Distribution by Treatment Condition",
        subtitle="Histogram with probability density normalized ",
        labels={"Expression": "Gene Expression", "Condition": "Treatment Condition"},
        hover_data=["Gene_ID"],
        opacity=0.75,
        file_path=str(output_path),
    )

    # Assertions to verify plot creation and file output
    assert fig is not None, "Figure object should not be None."
    assert output_path.exists(), f"Output file should exist: {output_path}"
    assert (
        output_path.stat().st_size > 0
    ), f"Output file should not be empty: {output_path}"
