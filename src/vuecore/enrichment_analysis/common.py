from __future__ import annotations

from collections.abc import Iterable

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
