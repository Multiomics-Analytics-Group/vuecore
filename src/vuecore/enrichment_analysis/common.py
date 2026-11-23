from __future__ import annotations

from collections.abc import Iterable
from logging import getLogger

import numpy as np
import pandas as pd

logger = getLogger(__name__)

DEFAULT_COMPARISON_SEPARATOR = "~"
DEFAULT_DIRECTION_COLORS = ["#cb181d", "#3288bd", "#ae017e", "#fcc5c0"]


def split_comparison_key(comparison_key: str, separator: str = "~") -> tuple[str, str]:
    """Split a key of the form 'group1~group2' into individual labels."""
    if separator not in comparison_key:
        return comparison_key, ""
    return comparison_key.split(separator, 1)


def format_comparison_title(
    base_title: str, comparison_key: str, separator: str = DEFAULT_COMPARISON_SEPARATOR
) -> str:
    """Build a readable figure title from base title and comparison key."""
    group_1, group_2 = split_comparison_key(comparison_key, separator)
    if not group_2:
        return f"{base_title} {group_1}"
    return f"{base_title} {group_1} vs {group_2}"


def build_color_map(
    values: Iterable[str],
    colors: dict[str, str] | list[str] | None = None,
) -> dict[str, str]:
    """Map each unique value in `values` to a color.

    If `colors` is a dict, it is returned as-is (a custom scheme). If it is a
    list (or omitted), unique values are assigned colors in order, cycling
    through the list if there are more values than colors.
    """
    if isinstance(colors, dict):
        return colors
    palette = colors if colors is not None else DEFAULT_DIRECTION_COLORS
    unique_values = sorted(set(values))
    return {value: palette[i % len(palette)] for i, value in enumerate(unique_values)}


PVALUE_LABEL = "-log10(padj)"
ODDS_RATIO_LABEL = "Lower bound of odds ratio (log scale)"


def select_comparison(df: pd.DataFrame, comparison: str | None) -> str:
    """Validate `comparison` against the 'comparison' column, inferring it if unique."""
    available = sorted(df["comparison"].unique())
    if comparison is None:
        if len(available) > 1:
            raise ValueError(
                "Multiple comparisons are available: "
                f"{', '.join(available)}. Pass `comparison` to select one."
            )
        return available[0]
    if comparison not in available:
        raise ValueError(
            f"Comparison '{comparison}' not found. Available comparisons: "
            f"{', '.join(available)}."
        )
    return comparison


def prepare_enrichment_data(
    df: pd.DataFrame, comparison: str, x: str | None = None
) -> tuple[pd.DataFrame, str]:
    """Select, rank and transform the rejected terms of one comparison.

    Adds the columns 'x' (plotted on the x-axis) and 'neg_log10_padj' (for
    color coding).

    Parameters
    ----------
    df : pd.DataFrame
        Validated enrichment results.
    comparison : str
        Comparison to keep.
    x : {'odds_ratio_lower', 'padj'}, optional
        Value for the x-axis. 'odds_ratio_lower' uses the lower bound of the
        odds ratio (to be shown on a log scale) and ranks terms by it; rows with
        a missing or zero lower bound cannot be shown on a log scale and are
        dropped with a warning. 'padj' uses -log10(padj). By default,
        'odds_ratio_lower' is used if any row has a lower bound above zero,
        otherwise 'padj'.

    Returns
    -------
    tuple[pd.DataFrame, str]
        Data sorted top to bottom, and the x mode that was used.
    """
    if x not in (None, "odds_ratio_lower", "padj"):
        raise ValueError(f"`x` must be 'odds_ratio_lower' or 'padj', got '{x}'.")
    df = df.query("comparison == @comparison and rejected").copy()
    if x is None:
        has_bound = (df["odds_ratio_lower"] > 0).any()
        x = "odds_ratio_lower" if has_bound else "padj"
        if not has_bound:
            logger.warning("No positive 'odds_ratio_lower' found, plotting padj.")
    df["neg_log10_padj"] = -np.log10(df["padj"])
    if x == "odds_ratio_lower":
        valid = df["odds_ratio_lower"] > 0  # False for NaN and 0
        if (~valid).any():
            logger.warning(
                f"Dropping {(~valid).sum()} term(s) with missing or zero "
                "'odds_ratio_lower', which cannot be shown on a log scale."
            )
        df = df.loc[valid]
        df["x"] = df["odds_ratio_lower"]
        sort_col = "odds_ratio_lower"
    else:
        df["x"] = df["neg_log10_padj"]
        sort_col = "padj"
    df = df.sort_values(by=["direction", sort_col], ascending=False).reset_index(
        drop=True
    )
    return df, x
