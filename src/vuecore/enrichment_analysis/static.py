# %%
from typing import Dict, Optional, Union

import matplotlib.figure
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from acore.types.enrichment_analysis import EnrichmentAnalysisSchema
from pandera.typing.pandas import DataFrame

from vuecore.enrichment_analysis.common import format_comparison_title
from vuecore.enrichment_analysis.interactive import (
    DIRECTION_COLORS,
    ENRICHMENT_HOVERING_COLS,
)

DEFAULT_DPI = 100


def _scale_marker_sizes(
    values: pd.Series, min_size: float = 60.0, max_size: float = 320.0
):
    """Scale foreground counts into matplotlib marker areas."""
    numeric = pd.to_numeric(values, errors="coerce").fillna(0)
    if numeric.empty:
        return []
    min_value = float(numeric.min())
    max_value = float(numeric.max())
    if max_value <= min_value:
        return [min_size] * len(numeric)
    scaled = (numeric - min_value) / (max_value - min_value)
    return (min_size + scaled * (max_size - min_size)).tolist()


def _build_static_enrichment_figure(
    df: pd.DataFrame,
    comparison_key: str,
    group: Optional[str],
    width: int,
    height: int,
    title: str,
    colors: Dict[str, str],
) -> matplotlib.figure.Figure:
    """Create one enrichment scatter plot as a matplotlib figure."""
    fig_width = max(width / DEFAULT_DPI, 4)
    fig_height = max(height / DEFAULT_DPI, 3)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=DEFAULT_DPI)

    y_positions = list(range(len(df)))
    marker_sizes = _scale_marker_sizes(df["foreground"])

    if group is None:
        ax.scatter(
            df["x"],
            y_positions,
            s=marker_sizes,
            alpha=0.7,
            linewidths=0.5,
            edgecolors="DarkSlateGrey",
            color="#4c78a8",
        )
    else:
        for group_value, group_df in df.groupby(group, sort=False):
            group_positions = [df.index.get_loc(idx) for idx in group_df.index]
            ax.scatter(
                group_df["x"],
                group_positions,
                s=_scale_marker_sizes(group_df["foreground"]),
                alpha=0.7,
                linewidths=0.5,
                edgecolors="DarkSlateGrey",
                color=colors.get(group_value, "#4c78a8"),
                label=group_value,
            )
        ax.legend(loc="upper right", frameon=False)

    ax.set_yticks(y_positions)
    ax.set_yticklabels(df["terms"])
    ax.set_xlabel("-log10(padj)")
    ax.set_ylabel("Enriched terms")
    ax.set_title(format_comparison_title(title, comparison_key))
    ax.grid(axis="x", linestyle="--", linewidth=0.5, alpha=0.4)
    ax.set_axisbelow(True)
    ax.invert_yaxis()
    fig.tight_layout()
    return fig


def get_enrichment_plot_static(
    enrichment_results: Union[pd.DataFrame, DataFrame[EnrichmentAnalysisSchema]],
    comparison: Optional[str] = None,
    width: int = 700,
    height: int = 500,
    title: str = "Enrichment",
    colors: Dict[str, str] = DIRECTION_COLORS,
    hovering_cols: list = ENRICHMENT_HOVERING_COLS,
) -> matplotlib.figure.Figure:
    """
    Create a static enrichment scatter plot for a single comparison based on an
    EnrichmentAnalysisSchema compliant DataFrame. The plot is rendered using matplotlib.

    Parameters
    ----------
    enrichment_results : Union[pd.DataFrame, DataFrame[EnrichmentAnalysisSchema]]
        Enrichment results validated against `EnrichmentAnalysisSchema`, with
        one or more comparisons stacked in the 'comparison' column.
    comparison : str, optional
        Comparison to plot. Required when more than one comparison is present;
        inferred automatically when there is only one.
    width : int, optional
        Plot width.
    height : int, optional
        Plot height.
    title : str, optional
        Base title for the plot.
    colors : dict[str, str], optional
        Color mapping by direction.
    hovering_cols : list, optional
        Accepted for API parity with the interactive version. Static figures do
        not render hover tooltips.

    Returns
    -------
    matplotlib.figure.Figure
        The scatter plot for the selected comparison.
    """

    df: pd.DataFrame = EnrichmentAnalysisSchema.validate(enrichment_results)

    available = sorted(df["comparison"].unique())
    if comparison is None:
        if len(available) > 1:
            raise ValueError(
                "Multiple comparisons are available: "
                f"{', '.join(available)}. Pass `comparison` to select one."
            )
        comparison = available[0]
    elif comparison not in available:
        raise ValueError(
            f"Comparison '{comparison}' not found. Available comparisons: "
            f"{', '.join(available)}."
        )

    df = df.query("comparison == @comparison and rejected").copy()
    df = df.sort_values(by=["direction", "padj"], ascending=False).reset_index(
        drop=True
    )
    df["x"] = -np.log10(df["padj"])

    return _build_static_enrichment_figure(
        df=df,
        comparison_key=comparison,
        group="direction",
        width=width,
        height=height,
        title=title,
        colors=colors,
    )


# %%
if __name__ == "__main__":
    # %%
    import pandas as pd

    fname = "/Users/heweb/Documents/repos/vuecore/tests/data/enrichment_analysis.csv"
    enrichment_results = pd.read_csv(fname, index_col=0)

    figure = get_enrichment_plot_static(
        enrichment_results, width=1500, height=800, title="Enrichment"
    )
    # figure

# %%
