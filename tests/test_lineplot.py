import pandas as pd
import pytest
from vuecore.plots.basic.line import create_line_plot


@pytest.fixture
def sample_line_df():
    """Fixture for generating sample data for a line plot."""
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
def test_basic_line_plot(sample_line_df, tmp_path, ext):
    """Test basic line plot creation with direct color mapping."""
    output_path = tmp_path / f"line_test.{ext}"

    fig = create_line_plot(
        data=sample_line_df,
        x="day",
        y="value",
        color="experiment",
        line_dash="condition",
        file_path=str(output_path),
    )

    assert fig is not None
    assert output_path.exists()
    assert output_path.stat().st_size > 0


@pytest.mark.parametrize("ext", ["png", "svg", "html", "json"])
def test_advanced_line_plot_refactored(sample_line_df, tmp_path, ext):
    """Test advanced line plot with new, more descriptive parameters."""
    output_path = tmp_path / f"line_test_advanced.{ext}"

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

    assert fig is not None
    assert output_path.exists()
    assert output_path.stat().st_size > 0
