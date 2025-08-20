import pandas as pd
import numpy as np
import pytest
from pathlib import Path

from vuecore.plots.basic.bar import create_bar_plot


@pytest.fixture
def sample_bar_data() -> pd.DataFrame:
    """
    Fixture for generating synthetic data for bar plots, replicating
    the code used in the docs/api_examples/bar_plot.ipynb example.
    Returns both the detailed abundance DataFrame and the aggregated
    DataFrame for the basic plot.
    """
    # Ensure reproducibility for tests
    np.random.seed(42)

    # Define sample types and bacterial genera
    sample_types = ["Soil", "Freshwater", "Ocean", "Sediment", "Wastewater"]
    genera = [
        "Pseudomonas",
        "Bacillus",
        "Escherichia",
        "Streptococcus",
        "Lactobacillus",
        "Bacteroides",
        "Clostridium",
        "Staphylococcus",
        "Enterobacter",
        "Klebsiella",
        "Salmonella",
        "Shigella",
        "Vibrio",
    ]

    def make_sample(sample: str, genera_list: list[str]) -> list[dict]:
        """
        Generate synthetic microbial abundance data for a single sample.
        Introduces variability in the number of genera per sample.
        """
        # Randomly pick a subset of genera to be present in this sample
        num_present_genera = np.random.randint(5, len(genera_list) + 1)
        selected_genera = np.random.choice(
            genera_list, num_present_genera, replace=False
        )

        # Generate random raw abundances for selected genera (shifted by +0.1 to avoid zeros)
        raw_abundances = np.random.rand(len(selected_genera)) + 0.1

        # Normalize abundances so they sum to exactly 100%
        relative_abundances = (raw_abundances / raw_abundances.sum()) * 100

        # Count how many genera are present
        genera_count = len(selected_genera)

        # Store results into list of dicts
        return [
            {
                "Sample": sample,
                "Genus": genus,
                "Relative_Abundance": abund,
                "Genera_Count": genera_count,
            }
            for genus, abund in zip(selected_genera, relative_abundances)
        ]

    # Generate the full detailed abundance DataFrame
    abund_df = pd.DataFrame(
        [row for sample in sample_types for row in make_sample(sample, genera)]
    )

    # Prepare data for the basic bar plot (genera count per sample)
    bar_plot_basic_df = abund_df.drop_duplicates(subset="Sample")[
        ["Sample", "Genera_Count"]
    ]

    # Return both DataFrames needed for testing
    return abund_df, bar_plot_basic_df


@pytest.mark.parametrize("ext", ["png", "svg", "html", "json"])
def test_basic_bar_plot(sample_bar_data: pd.DataFrame, tmp_path: Path, ext: str):
    """
    Test basic bar plot creation, ensuring the figure is returned,
    and output files are generated correctly for various formats.
    """
    # Unpack the fixture data
    _, bar_plot_basic_df = sample_bar_data

    # Define the output path using tmp_path fixture for temporary files
    output_path = tmp_path / f"basic_bar_test.{ext}"

    # Create the basic bar plot using the VueCore function
    fig = create_bar_plot(
        data=bar_plot_basic_df,
        x="Sample",
        y="Genera_Count",
        title="Genera Count by Sample Type",
        file_path=str(output_path),
    )

    # Assertions to verify plot creation and file output
    assert fig is not None, "Figure object should not be None."
    assert output_path.exists(), f"Output file should exist: {output_path}"
    assert (
        output_path.stat().st_size > 0
    ), f"Output file should not be empty: {output_path}"


@pytest.mark.parametrize("ext", ["png", "svg", "html", "json"])
def test_advanced_bar_plot(sample_bar_data: pd.DataFrame, tmp_path: Path, ext: str):
    """
    Test advanced stacked bar plot creation with multiple parameters,
    ensuring the figure is returned and output files are generated.
    """
    # Unpack the fixture data
    abund_df, _ = sample_bar_data

    # Define the output path for the advanced plot
    output_path = tmp_path / f"advanced_bar_test.{ext}"

    # Create the advanced stacked bar plot using the VueCore function
    fig = create_bar_plot(
        data=abund_df,
        x="Sample",
        y="Relative_Abundance",
        color="Genus",
        barmode="stack",
        title="Taxonomic Profile of Environmental Samples",
        subtitle="Relative Abundance of Bacterial Genera",
        labels={
            "Sample": "Environmental Sample Type",
            "Relative_Abundance": "Relative Abundance (%)",
            "Genus": "Genus",
        },
        hover_name="Genus",
        hover_data=["Relative_Abundance"],
        opacity=0.9,
        file_path=str(output_path),
    )

    # Assertions to verify plot creation and file output
    assert fig is not None, "Figure object should not be None."
    assert output_path.exists(), f"Output file should exist: {output_path}"
    assert (
        output_path.stat().st_size > 0
    ), f"Output file should not be empty: {output_path}"
