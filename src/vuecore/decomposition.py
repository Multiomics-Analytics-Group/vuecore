"""Decompositon plots like pca, umap, tsne, etc."""

import itertools
from typing import Optional

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import sklearn.decomposition


def plot_explained_variance(
    pca: sklearn.decomposition.PCA, ax: Optional[matplotlib.axes.Axes] = None
) -> matplotlib.axes.Axes:
    """Plot explained variance of PCA from scikit-learn."""
    exp_var = pd.Series(pca.explained_variance_ratio_).to_frame("explained variance")
    exp_var.index += 1  # start at 1
    exp_var["explained variance (cummulated)"] = exp_var["explained variance"].cumsum()
    exp_var.index.name = "PC"
    ax = exp_var.plot(ax=ax)
    return ax


def pca_grid(
    PCs: pd.DataFrame,
    meta_column: pd.Series,
    n_components: int = 4,
    meta_col_name: Optional[str] = None,
    figsize=(6, 8),
) -> plt.Figure:
    """Plot a grid of scatter plots for the first n_components of PCA,  per default 4.

    Parameters
    ----------
    PCs : pd.DataFrame
        DataFrame with the principal components as columns.
    meta_column : pd.Series
        Series with categorical data to color the scatter plots.
    n_components : int, optional
        Number of first n components to plot, by default 4
    meta_col_name : Optional[str], optional
        If another name than the default series name shoudl be used, by default None

    Returns
    -------
    plt.Figure
        Matplotlib figure with the scatter plots.
    """
    if meta_col_name is None:
        meta_col_name = meta_column.name
    else:
        meta_column = meta_column.rename(meta_col_name)
    up_to = min(PCs.shape[-1], n_components)
    fig, axes = plt.subplots(up_to - 1, 2, figsize=figsize, layout="constrained")
    PCs = PCs.join(
        meta_column.astype("category")
    )  # ! maybe add a check that it's not continous
    for k, (pos, ax) in enumerate(
        zip(itertools.combinations(range(up_to), 2), axes.flatten())
    ):
        i, j = pos
        plot_heatmap = bool(k % 2)
        PCs.plot.scatter(
            i,
            j,
            c=meta_col_name,
            cmap="Paired",
            ax=ax,
            colorbar=plot_heatmap,
        )
    return fig
