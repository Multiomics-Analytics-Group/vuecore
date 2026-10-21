from __future__ import annotations

from collections.abc import Iterable

import pandas as pd
from acore.types.exploratory_analysis import TwoComponentSchema, TwoLoadingsSchema
from pandera.typing.pandas import DataFrame

DEFAULT_GROUP_COLORS = [
    "#4c78a8",
    "#f58518",
    "#54a24b",
    "#e45756",
    "#72b7b2",
    "#eeca3b",
    "#b279a2",
    "#ff9da6",
    "#9d755d",
    "#bab0ac",
]
DEFAULT_LOADING_COLOR = "darkgrey"


def build_color_map(
    values: Iterable[str],
    colors: dict[str, str] | list[str] | None = None,
) -> dict[str, str]:
    """Map each unique value in `values` to a color.

    Parameters
    ----------
    values : Iterable[str]
        Group labels, e.g. the 'group' column of the components.
    colors : dict[str, str] or list[str], optional
        A dict is returned as-is (a custom scheme). A list (or the default
        palette if omitted) is assigned to the sorted unique values in order,
        cycling through it if there are more values than colors.

    Returns
    -------
    dict[str, str]
        Mapping of group label to color.
    """
    if isinstance(colors, dict):
        return colors
    palette = colors if colors is not None else DEFAULT_GROUP_COLORS
    unique_values = sorted(set(values))
    return {value: palette[i % len(palette)] for i, value in enumerate(unique_values)}


def select_top_loadings(loadings: pd.DataFrame, top_n: int) -> pd.DataFrame:
    """Select the `top_n` features with the highest loading 'value'.

    If 'value' is missing, it is computed as the length of the loading vector,
    as `acore.exploratory_analysis.run_pca` does.
    """
    if "value" not in loadings.columns:
        loadings = loadings.assign(
            value=(loadings["x"] ** 2 + loadings["y"] ** 2) ** 0.5
        )
    return loadings.nlargest(top_n, "value")


def get_loading_scale_factor(
    components: pd.DataFrame,
    loadings: pd.DataFrame,
    x: str = "x",
    y: str = "y",
    fraction: float = 0.8,
) -> float:
    """Factor to stretch the loadings onto the range of the components.

    The longest loading arrow reaches `fraction` of the largest absolute
    component value, so arrows and samples share one set of axes.

    Parameters
    ----------
    components : pd.DataFrame
        Sample coordinates with columns `x` and `y`.
    loadings : pd.DataFrame
        Feature loadings with columns `x` and `y`.
    x, y : str, optional
        Column names of the two dimensions in both DataFrames.
    fraction : float, optional
        Fraction of the components' range the longest arrow should reach.

    Returns
    -------
    float
        Scale factor to multiply the loadings with.
    """
    max_component = components[[x, y]].abs().to_numpy().max()
    max_loading = (loadings[x] ** 2 + loadings[y] ** 2).pow(0.5).max()
    if not max_loading:
        return 1.0
    return fraction * max_component / max_loading


def prepare_embedding_data(
    components: pd.DataFrame | DataFrame[TwoComponentSchema],
    loadings: pd.DataFrame | DataFrame[TwoLoadingsSchema] | None = None,
    group: str | None = "group",
    top_n_loadings: int = 15,
    loading_factor: float | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame | None]:
    """Validate a 2D embedding and scale the loadings for plotting.

    Parameters
    ----------
    components : DataFrame[TwoComponentSchema]
        Sample coordinates in the columns 'x' and 'y', e.g. the first result of
        `acore.exploratory_analysis.run_pca` or the result of `run_tsne` or
        `run_umap`.
    loadings : DataFrame[TwoLoadingsSchema], optional
        Feature loadings in the columns 'x' and 'y' with the feature names in the
        index and the loading strength in 'value'. Only meaningful for PCA.
    group : str, optional
        Column in `components` used to color the samples. Pass `None` to plot all
        samples in one color.
    top_n_loadings : int, optional
        Number of features with the highest loading 'value' to keep.
    loading_factor : float, optional
        Factor the loadings are multiplied with. If omitted, it is chosen so that
        the longest arrow reaches 80% of the components' range.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame | None]
        The validated components and the selected, scaled loadings (or `None`).

    Raises
    ------
    pandera.errors.SchemaError
        If `components` or `loadings` do not match their schema.
    ValueError
        If `group` is not a column of `components`.
    """
    df: pd.DataFrame = TwoComponentSchema.validate(components)
    if group is not None and group not in df.columns:
        raise ValueError(
            f"Group column '{group}' not found. Available columns: "
            f"{', '.join(map(str, df.columns))}. Pass group=None to plot without "
            "groups."
        )
    if loadings is None:
        return df, None

    loadings = TwoLoadingsSchema.validate(loadings)
    loadings = select_top_loadings(loadings, top_n_loadings)
    if loading_factor is None:
        loading_factor = get_loading_scale_factor(df, loadings)
    loadings = loadings.assign(
        x=loadings["x"] * loading_factor, y=loadings["y"] * loading_factor
    )
    return df, loadings
