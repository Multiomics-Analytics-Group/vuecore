from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Iterator, Mapping, Tuple, Union

import numpy as np
import pandas as pd

DEFAULT_COMPARISON_KEY = "regulated~non-regulated"
DEFAULT_OUTPUT_PREFIX = "enrichment"
REQUIRED_COLUMNS = ("terms", "padj", "rejected", "foreground")
INTERACTIVE_OUTPUT_FORMATS = frozenset({"html", "json"})
STATIC_OUTPUT_FORMATS = frozenset({"png", "svg", "pdf", "webp", "jpg", "jpeg"})


def normalize_enrichment_results(
    enrichment_results: Union[pd.DataFrame, Mapping[str, pd.DataFrame]],
) -> Dict[str, pd.DataFrame]:
    """Normalize input to a dict keyed by pairwise comparison."""
    if isinstance(enrichment_results, pd.DataFrame):
        return {DEFAULT_COMPARISON_KEY: enrichment_results.copy()}

    if isinstance(enrichment_results, Mapping):
        normalized: Dict[str, pd.DataFrame] = {}
        for key, table in enrichment_results.items():
            if not isinstance(table, pd.DataFrame):
                raise TypeError(
                    "enrichment_results values must be pandas DataFrame objects"
                )
            normalized[str(key)] = table.copy()
        return normalized

    raise TypeError(
        "enrichment_results must be a pandas DataFrame or mapping[str, DataFrame]"
    )


def _validate_required_columns(table: pd.DataFrame, comparison_key: str) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in table.columns]
    if missing:
        missing_str = ", ".join(missing)
        raise ValueError(
            f"Missing required columns for '{comparison_key}': {missing_str}"
        )


def prepare_enrichment_tables(
    enrichment_results: Union[pd.DataFrame, Mapping[str, pd.DataFrame]],
) -> Iterator[Tuple[str, pd.DataFrame, str, str, str]]:
    """
    Yield normalized and filtered enrichment tables.

    Returns
    -------
    Iterator[Tuple[str, pd.DataFrame, str, str, str]]
        comparison key, prepared dataframe, group1 label, group2 label, and
        optional grouping column ("direction" when available).
    """
    normalized = normalize_enrichment_results(enrichment_results)

    for comparison_key in sorted(normalized):
        table = normalized[comparison_key]

        if table.empty:
            continue

        _validate_required_columns(table=table, comparison_key=comparison_key)

        df = table[table["rejected"].astype(bool)].copy()
        if df.empty:
            continue

        group = "direction" if "direction" in df.columns else None
        sort_cols = ["padj"] if group is None else [group, "padj"]
        df = df.sort_values(by=sort_cols, ascending=False).reset_index(drop=True)

        min_positive = np.finfo(float).tiny
        df["x"] = -np.log10(
            pd.to_numeric(df["padj"], errors="coerce").clip(lower=min_positive)
        )

        group_1, group_2 = split_comparison_key(comparison_key)
        yield comparison_key, df, group_1, group_2, group


def split_comparison_key(comparison_key: str) -> Tuple[str, str]:
    """Split a key of the form 'group1~group2' into individual labels."""
    if "~" not in comparison_key:
        return comparison_key, ""
    return comparison_key.split("~", 1)


def format_comparison_title(base_title: str, comparison_key: str) -> str:
    """Build a readable figure title from base title and comparison key."""
    group_1, group_2 = split_comparison_key(comparison_key)
    if not group_2:
        return f"{base_title} {group_1}"
    return f"{base_title} {group_1} vs {group_2}"


def comparison_slug(comparison_key: str) -> str:
    """Create a stable filesystem-safe comparison slug."""
    slug = comparison_key.replace("~", "_vs_")
    slug = re.sub(r"[^A-Za-z0-9._-]", "_", slug)
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug or "comparison"


def build_output_path(
    output_folder: Union[str, Path],
    comparison_key: str,
    output_format: str,
    output_prefix: str = DEFAULT_OUTPUT_PREFIX,
) -> Path:
    """Build a deterministic output path for one comparison plot."""
    ext = output_format.lstrip(".").lower()
    if not ext:
        raise ValueError("output_format must not be empty")

    folder = Path(output_folder)
    filename = f"{output_prefix}_{comparison_slug(comparison_key)}.{ext}"
    return folder / filename


def validate_output_format(output_format: str, allowed_formats: frozenset[str]) -> str:
    """Normalize and validate an output format against an allowed set."""
    normalized = output_format.lstrip(".").lower()
    if normalized not in allowed_formats:
        allowed = ", ".join(sorted(allowed_formats))
        raise ValueError(
            f"Unsupported output_format '{output_format}'. Allowed formats: {allowed}"
        )
    return normalized
