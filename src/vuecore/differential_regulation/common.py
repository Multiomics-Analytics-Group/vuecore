from __future__ import annotations

from logging import getLogger

import numpy as np
import pandas as pd
from acore.types.differential_analysis import (
    AncovaSchema,
    AnovaSchema,
    AnovaSchemaMultiGroup,
)
from pandera.typing.pandas import DataFrame

DEFAULT_COMPARISON_SEPARATOR = "~"
NOT_REGULATED = "not regulated"
DEFAULT_NOT_REGULATED_COLOR = "lightgrey"
DEFAULT_GROUP_COLORS = ["#3288bd", "#cb181d"]

logger = getLogger(__name__)


def validate_differential_regulation(
    data: (
        DataFrame[AnovaSchema]
        | DataFrame[AnovaSchemaMultiGroup]
        | DataFrame[AncovaSchema]
    ),
) -> pd.DataFrame:
    """Validate against the two- or multi-group schema, depending on the columns.

    Results of an ANOVA with more than two groups carry the 'posthoc ...' columns
    and are validated against `AnovaSchemaMultiGroup`, all others against
    `AnovaSchema`. Feature identifiers are expected in the index.
    """
    if "posthoc Paired" in data.columns:
        return AnovaSchemaMultiGroup.validate(data)
    elif "coef" in data.columns:
        return AncovaSchema.validate(data)
    return AnovaSchema.validate(data)


def add_comparison_column(
    df: pd.DataFrame, separator: str = DEFAULT_COMPARISON_SEPARATOR
) -> tuple[pd.DataFrame, str]:
    """Return a copy and the column containing comparison identifiers."""
    if "comparison" in df.columns:
        logger.warning(
            "The input DataFrame already has a 'comparison' column, so none is added."
        )
        return df, "comparison"
    if "posthoc comparison" in df.columns:
        logger.warning(
            "The input DataFrame has a 'posthoc comparison' column; adding a "
            "standardized 'comparison' column from 'group1' and 'group2'."
        )
    df = df.copy()
    df["comparison"] = df["group1"] + separator + df["group2"]
    return df, "comparison"


def assign_regulation(
    df: pd.DataFrame,
    group1: str,
    group2: str,
    col_rejected: str = "rejected",
    col_log2fc: str = "log2FC",
) -> pd.Series:
    """Label each row as 'upregulated in <group>' or 'not regulated'.

    Rejected rows with a positive fold change are 'upregulated in group1', those with a
    negative one 'upregulated in group2'; everything else is 'not regulated'.
    """
    rejected = df[col_rejected].astype(bool)
    return pd.Series(
        np.select(
            [rejected & (df[col_log2fc] > 0), rejected & (df[col_log2fc] < 0)],
            [f"upregulated in {group1}", f"upregulated in {group2}"],
            default=NOT_REGULATED,
        ),
        index=df.index,
        name="regulation",
    )


def label_top_n(df: pd.DataFrame, col_sort: str, top_n: int) -> pd.Series:
    """Index values of the `top_n` rows with the smallest `col_sort`, else ''."""
    labels = pd.Series("", index=df.index, name="label", dtype=object)
    top = df[col_sort].nsmallest(top_n).index
    labels.loc[top] = top.astype(str)
    return labels


def format_comparison_title(
    base_title: str, comparison_key: str, separator: str = DEFAULT_COMPARISON_SEPARATOR
) -> str:
    """Build a readable figure title from base title and comparison key."""
    if separator not in comparison_key:
        return f"{base_title} {comparison_key}"
    group_1, group_2 = comparison_key.split(separator, 1)
    return f"{base_title} {group_1} vs {group_2}"


def build_color_map(
    group1: str,
    group2: str,
    colors: dict[str, str] | list[str] | None = None,
) -> dict[str, str]:
    """Map the regulation labels to colors.

    A dict is returned as-is. A list of two colors is used for 'upregulated in group1' and
    'upregulated in group2' (in that order); 'not regulated' is always light grey.
    """
    if isinstance(colors, dict):
        return colors
    palette = colors if colors is not None else DEFAULT_GROUP_COLORS
    return {
        NOT_REGULATED: DEFAULT_NOT_REGULATED_COLOR,
        f"upregulated in {group1}": palette[0],
        f"upregulated in {group2}": palette[1],
    }
