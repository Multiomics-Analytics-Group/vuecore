import pandas as pd
import pytest
from pathlib import Path

from vuecore.plots.basic.line import create_line_plot


@pytest.fixture
def sample_line_df() -> pd.DataFrame:
    """
    Fixture for generating synthetic data for line plots, replicating
    the code used in the docs/api_examples/line_plot.ipynb example.
    """
    data = pd.DataFrame(
        {
            "day": list(range(1, 6)) * 4,  # 5 days
            "experiment": ["A"] * 10 + ["B"] * 10,  # 2 experiments
            "condition": (["Control"] * 5 + ["Treatment"] * 5) * 2,  # 2 conditions
            "value": [
                11,
                13,
                15,
                17,
                18,  # A - Control
                10,
                12,
                14,
                15,
                16,  # A - Treatment
                19,
                20,
                21,
                22,
                23,  # B - Control
                20,
                22,
                21,
                23,
                22,  # B - Treatment
            ],
            "value_error": [
                1,
                1.2,
                0.9,
                1.1,
                1.0,
                1.3,
                1.0,
                1.2,
                1.4,
                1.1,
                2.0,
                1.8,
                2.1,
                1.5,
                2.3,
                1.7,
                2.0,
                1.8,
                2.1,
                2.2,
            ],
        }
    )
    return pd.DataFrame(data)


@pytest.mark.parametrize("ext", ["png", "svg", "html", "json"])
def test_basic_line_plot(sample_line_df: pd.DataFrame, tmp_path: Path, ext: str):
    """
    Test basic line plot creation, ensuring the figure is returned,
    and output files are generated correctly for various formats.
    """
    # Define the output path using tmp_path fixture for temporary files
    output_path = tmp_path / f"line_test.{ext}"

    # Create the basic line plot using the VueCore function
    fig = create_line_plot(
        data=sample_line_df,
        x="day",
        y="value",
        color="experiment",
        line_dash="condition",
        file_path=str(output_path),
    )

    # Assertions to verify plot creation and file output
    assert fig is not None, "Figure object should not be None."
    assert output_path.exists(), f"Output file should exist: {output_path}"
    assert (
        output_path.stat().st_size > 0
    ), f"Output file should not be empty: {output_path}"


@pytest.mark.parametrize("ext", ["png", "svg", "html", "json"])
def test_advanced_line_plot(sample_line_df: pd.DataFrame, tmp_path: Path, ext: str):
    """
    Test advanced line plot creation with multiple parameters,
    ensuring the figure is returned and output files are generated.
    """
    # Define the output path for the advanced plot
    output_path = tmp_path / f"line_test_advanced.{ext}"

    # Create the advanced line plot using the VueCore function
    fig = create_line_plot(
        data=sample_line_df,
        x="day",
        y="value",
        color="experiment",
        line_dash="condition",
        error_y="value_error",
        title="Experiment & Condition Trends",
        labels={"day": "Day", "value": "Response", "condition": "Condition"},
        color_discrete_map={"A": "#508AA8", "B": "#A8505E"},
        line_dash_map={"Control": "solid", "Treatment": "dot"},
        markers=True,
        line_shape="spline",
        file_path=str(output_path),
    )

    # Assertions to verify plot creation and file output
    assert fig is not None, "Figure object should not be None."
    assert output_path.exists(), f"Output file should exist: {output_path}"
    assert (
        output_path.stat().st_size > 0
    ), f"Output file should not be empty: {output_path}"
