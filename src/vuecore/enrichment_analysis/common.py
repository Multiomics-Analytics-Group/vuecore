from typing import Tuple


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
