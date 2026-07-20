import pandas as pd
import numpy as np
import pytest
from pathlib import Path

from vuecore.plots.basic.violin import create_violin_plot


@pytest.fixture
def sample_violin_data() -> pd.DataFrame:
    """
    Fixture for generating synthetic data for violin plots, replicating
    the code used in the docs/api_examples/box_violin_plot.ipynb example.
    """
    # Set a random seed for reproducibility of the synthetic data
    np.random.seed(42)

    # Parameters
    num_samples = 200
    sample_groups = ["Patient A", "Patient B", "Patient C", "Patient D"]
    treatments = ["Control", "Treated"]

    # Sample metadata
    sample_ids = np.random.choice(sample_groups, size=num_samples)
    treatment_assignments = np.random.choice(treatments, size=num_samples)
    gene_ids = [f"Gene_{g}" for g in np.random.randint(1, 1500, size=num_samples)]

    # Base expression values
    base_expr = np.random.normal(loc=100, scale=35, size=num_samples)

    # Treatment effect simulation
    treatment_effect = np.where(
        treatment_assignments == "Treated",
        np.random.normal(loc=50, scale=30, size=num_samples),
        0,
    )

    # Small random per-gene offset for extra variability
    gene_offset = np.random.normal(loc=0, scale=20, size=num_samples)

    # Final expression
    expr = base_expr + treatment_effect + gene_offset

    # Construct DataFrame
    gene_exp_df = pd.DataFrame(
        {
            "Sample_ID": sample_ids,
            "Treatment": treatment_assignments,
            "Gene_ID": gene_ids,
            "Expression": expr,
        }
    )

    return gene_exp_df


@pytest.mark.parametrize("ext", ["png", "svg", "html", "json"])
def test_basic_violin_plot(sample_violin_data: pd.DataFrame, tmp_path: Path, ext: str):
    """
    Test basic violin plot creation, ensuring the figure is returned,
    and output files are generated correctly for various formats.
    """
    # Define the output path using tmp_path fixture for temporary files
    output_path = tmp_path / f"basic_violin_test.{ext}"

    # Create the basic violin plot using the VueCore function
    fig = create_violin_plot(
        data=sample_violin_data,
        x="Treatment",
        y="Expression",
        title="Gene Expression Levels by Treatment",
        file_path=str(output_path),
    )

    # Assertions to verify plot creation and file output
    assert fig is not None, "Figure object should not be None."
    assert output_path.exists(), f"Output file should exist: {output_path}"
    assert (
        output_path.stat().st_size > 0
    ), f"Output file should not be empty: {output_path}"


@pytest.mark.parametrize("ext", ["png", "svg", "html", "json"])
def test_advanced_violin_plot(
    sample_violin_data: pd.DataFrame, tmp_path: Path, ext: str
):
    """
    Test advanced violin plot creation with multiple parameters,
    ensuring the figure is returned and output files are generated.
    """
    # Define the output path for the advanced plot
    output_path = tmp_path / f"advanced_violin_test.{ext}"

    # Create the advanced violin plot using the VueCore function
    fig = create_violin_plot(
        data=sample_violin_data,
        x="Treatment",
        y="Expression",
        color="Sample_ID",
        violinmode="group",
        points="outliers",
        title="Gene Expression Levels with Control and Treatment Condition",
        subtitle="Distribution of gene expression across different treatments and patient samples",
        labels={
            "Treatment": "Treatment",
            "Expression": "Gene Expression",
            "Sample_ID": "Patient Sample ID",
        },
        color_discrete_map={
            "Patient A": "#508AA8",
            "Patient B": "#A8505E",
            "Patient C": "#86BF84",
            "Patient D": "#A776AF",
        },
        category_orders={
            "Sample_ID": ["Patient A", "Patient B", "Patient C", "Patient D"]
        },
        hover_data=["Gene_ID"],
        file_path=str(output_path),
    )

    # Assertions to verify plot creation and file output
    assert fig is not None, "Figure object should not be None."
    assert output_path.exists(), f"Output file should exist: {output_path}"
    assert (
        output_path.stat().st_size > 0
    ), f"Output file should not be empty: {output_path}"
