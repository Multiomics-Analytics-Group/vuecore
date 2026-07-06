# %%
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Union

import matplotlib.figure
import matplotlib.pyplot as plt
import pandas as pd

from vuecore.enrichment_analysis.common import (
    STATIC_OUTPUT_FORMATS,
    build_output_path,
    format_comparison_title,
    prepare_enrichment_tables,
    validate_output_format,
)
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


def _save_matplotlib_figure(
    fig: matplotlib.figure.Figure,
    output_path: Path,
    output_format: str,
    dpi: int = DEFAULT_DPI,
) -> None:
    """Save a matplotlib figure with a format inferred from the API contract."""
    fig.savefig(output_path, format=output_format, bbox_inches="tight", dpi=dpi)


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


def create_enrichment_plots_static(
    enrichment_results: Union[pd.DataFrame, Mapping[str, pd.DataFrame]],
    output_folder: Optional[str] = None,
    output_format: str = "png",
    width: int = 900,
    height: int = 800,
    title: str = "Enrichment",
    colors: Dict[str, str] = DIRECTION_COLORS,
    hovering_cols: list = ENRICHMENT_HOVERING_COLS,
) -> Dict[str, Dict[str, Any]]:
    """
    Create enrichment scatter plots and optionally save static files per comparison.

    Parameters
    ----------
    enrichment_results : pd.DataFrame or mapping[str, pd.DataFrame]
        One enrichment table or dictionary keyed by comparison label.
    output_folder : str, optional
        Directory where files are written. If omitted, no files are saved.
    output_format : str, optional
        Static format (png, svg, pdf, webp, jpg, jpeg). Default is "png".
    width : int, optional
        Plot width.
    height : int, optional
        Plot height.
    title : str, optional
        Base title for all plots.
    colors : dict[str, str], optional
        Color mapping by direction/group.
    hovering_cols : list, optional
        Accepted for API parity with the interactive version. Static figures do
        not render hover tooltips.

    Returns
    -------
    dict[str, dict[str, Any]]
        Mapping from comparison key to payload containing the figure and output path.
    """
    normalized_output_format = validate_output_format(
        output_format=output_format,
        allowed_formats=STATIC_OUTPUT_FORMATS,
    )
    results: Dict[str, Dict[str, Any]] = {}

    for comparison_key, df, _, _, group in prepare_enrichment_tables(
        enrichment_results
    ):
        fig = _build_static_enrichment_figure(
            df=df,
            comparison_key=comparison_key,
            group=group,
            width=width,
            height=height,
            title=title,
            colors=colors,
        )

        output_path = None
        if output_folder:
            output_path = build_output_path(
                output_folder=output_folder,
                comparison_key=comparison_key,
                output_format=normalized_output_format,
            )
            output_path.parent.mkdir(parents=True, exist_ok=True)
            _save_matplotlib_figure(
                fig=fig,
                output_path=output_path,
                output_format=normalized_output_format,
            )

        results[comparison_key] = {
            "figure": fig,
            "output_path": str(output_path) if output_path else None,
        }

    return results


# %%
if __name__ == "__main__":
    # %%
    import pandas as pd

    fname = "/Users/heweb/Documents/repos/vuecore/tests/data/enrichment_analysis.csv"
    enrichment_results = pd.read_csv(fname, index_col=0)

    figures = create_enrichment_plots_static(
        enrichment_results, width=1500, height=800, title="Enrichment"
    )
    figures["regulated~non-regulated"]["figure"]

# %%
