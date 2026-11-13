from __future__ import annotations

from collections.abc import Iterable

import pandas as pd
from acore.types.exploratory_analysis import (
    AnnotationResult,
    TwoComponentSchema,
    TwoLoadingsSchema,
)
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


def select_top_loadings(
    loadings: pd.DataFrame, top_n: int, x: str = "x", y: str = "y"
) -> pd.DataFrame:
    """Select the `top_n` features with the highest loading 'value'.

    If 'value' is missing, it is computed as the length of the loading vector in
    the dimensions `x` and `y`. `acore.exploratory_analysis.run_pca` computes
    'value' over all components instead.
    """
    if "value" not in loadings.columns:
        loadings = loadings.assign(value=(loadings[x] ** 2 + loadings[y] ** 2) ** 0.5)
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


def unpack_results(
    results: pd.DataFrame | tuple | list | dict,
    loadings: pd.DataFrame | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame | None]:
    """Get the components and loadings from the output of an acore function.

    Parameters
    ----------
    results : pd.DataFrame, tuple, list or dict
        One of:

        - the components DataFrame itself,
        - the `(components, loadings, variance)` tuple of
          `acore.exploratory_analysis.run_pca`,
        - the dictionary with one DataFrame of `run_tsne` or `run_umap`, e.g.
          `{"umap": components}`.
    loadings : pd.DataFrame, optional
        Loadings which take precedence over the ones found in `results`.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame | None]
        The components and the loadings (or `None`).

    Raises
    ------
    ValueError
        If `results` is none of the supported structures.
    """
    if isinstance(results, pd.DataFrame):
        components, found = results, None
    elif isinstance(results, dict) and len(results) == 1:
        components, found = next(iter(results.values())), None
    elif isinstance(results, (tuple, list)) and len(results) == 3:
        components, found, _variance = results
    else:
        raise ValueError(
            "results must be a DataFrame, the (components, loadings, variance) "
            "tuple of run_pca or the one-entry dictionary of run_tsne / run_umap, "
            f"got {type(results).__name__}"
            + (f" with {len(results)} entries." if hasattr(results, "__len__") else ".")
        )
    return components, loadings if loadings is not None else found


def get_axis_titles(
    annotation: AnnotationResult | dict | None,
    x: str = "x",
    y: str = "y",
    x_title: str | None = None,
    y_title: str | None = None,
) -> tuple[str, str]:
    """Axis titles for the columns `x` and `y`.

    An explicit title wins, then the readable name in the `annotation` of the
    acore function, then the column name itself.
    """
    if isinstance(annotation, AnnotationResult):
        annotation = annotation.model_dump(exclude_none=True)
    names = annotation or {}
    return x_title or names.get(x, x), y_title or names.get(y, y)


def _check_columns(df: pd.DataFrame, columns: list[str], name: str) -> None:
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(
            f"Column(s) {missing} not found in {name}. Available columns: "
            f"{', '.join(map(str, df.columns))}."
        )


def prepare_embedding_data(
    components: pd.DataFrame | DataFrame[TwoComponentSchema],
    loadings: pd.DataFrame | DataFrame[TwoLoadingsSchema] | None = None,
    group: str | None = "group",
    top_n_loadings: int = 15,
    loading_factor: float | None = None,
    x: str = "x",
    y: str = "y",
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
    x, y : str, optional
        Columns of the dimensions to plot, e.g. 'x' and 'z' for the first and
        third component.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame | None]
        The validated components and the selected, scaled loadings (or `None`).

    Raises
    ------
    pandera.errors.SchemaError
        If `components` or `loadings` do not match their schema.
    ValueError
        If `group`, `x` or `y` is not a column of `components` (or `loadings`).
    """
    df: pd.DataFrame = TwoComponentSchema.validate(components)
    _check_columns(df, [x, y], "components")
    if group is not None and group not in df.columns:
        raise ValueError(
            f"Group column '{group}' not found. Available columns: "
            f"{', '.join(map(str, df.columns))}. Pass group=None to plot without "
            "groups."
        )
    if loadings is None:
        return df, None

    loadings = TwoLoadingsSchema.validate(loadings)
    _check_columns(loadings, [x, y], "loadings")
    loadings = select_top_loadings(loadings, top_n_loadings, x=x, y=y)
    if loading_factor is None:
        loading_factor = get_loading_scale_factor(df, loadings, x=x, y=y)
    loadings = loadings.assign(
        **{x: loadings[x] * loading_factor, y: loadings[y] * loading_factor}
    )
    return df, loadings
