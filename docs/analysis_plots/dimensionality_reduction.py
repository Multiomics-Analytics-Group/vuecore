# %% [markdown]
# # Dimensionality Reduction Plots
#
# Runs a PCA and a UMAP on the iris dataset using acore and presents the current plotting
# functions for a 2D embedding. The functions are available in the
# [`vuecore.dimensionality_reduction` module](vuecore.dimensionality_reduction).
#
# ## Overview
# For both static and interactive versions of the plots:
# - show acore related function that checks the input for compatibility
#   ([`TwoComponentSchema`](acore.types.exploratory_analysis.TwoComponentSchema) and,
#   for PCA, [`TwoLoadingsSchema`](acore.types.exploratory_analysis.TwoLoadingsSchema))
#   and calls the backend specific plotting function with the required parameters.
#   The same function is used for PCA, t-SNE and UMAP results.
# - show manually calling the backend specific plotting function with the required
#   parameters. For these, the setup of the data is the responsibility of the user. The
#   function will not check for compatibility and accepts [`DataFrame`s](pandas.DataFrame)
#   with only the required columns for that plot.

# %% tags=["hide-output"]
# %pip install vuecore


# %% tags=["hide-input"]
import numpy as np
import pandas as pd
from acore.exploratory_analysis import run_pca, run_umap

from vuecore.dimensionality_reduction import (
    get_embedding_plot_interactive,
    get_embedding_plot_static,
)
from vuecore.dimensionality_reduction.interactive import get_embedding_plot_plotly
from vuecore.dimensionality_reduction.static import (
    DEFAULT_DPI,
    get_embedding_plot_mpl,
)

# %% [markdown]
# # Load example data
# - the iris dataset: four measured features for 150 flowers of three species
# - samples are rows, features are columns, with the additional columns `group`
#   (the species) and `sample` (an identifier) as expected by acore

# %% tags=["hide-input"]
BASE = (
    "https://raw.githubusercontent.com/RasmussenLab/njab/"
    "HEAD/docs/tutorial/data/alzheimer/"
)
META: str = "meta.csv"  # clincial data
CLINIC_ML: str = "clinic_ml.csv"  # clinical data
OMICS: str = "proteome.csv"  # omics data
data = pd.read_csv(f"{BASE}{OMICS}", sep=",", header=0, index_col=0).convert_dtypes()
data = np.log2(data + 1)  # log2 transform the data
group = pd.read_csv(
    f"{BASE}{META}",
    sep=",",
    header=0,
    index_col=0,
    usecols=["Sample ID", "_collection site"],
).convert_dtypes()
data = group.dropna().rename(columns={"_collection site": "group"}).join(data)
data.head()

# %% [markdown]
# ## Run PCA and UMAP using acore
# Both return the sample coordinates in the columns `x` and `y`, together with `group` and
# the annotation columns. The PCA additionally returns the loadings of each feature and
# the explained variance, and both return axis titles in `args`.

# %%
(components, loadings, explained_variance), pca_args = run_pca(
    data,
    group="group",
    annotation_cols=[],
)
pca_args

# %%
components

# %%
loadings

# %%
umap_result, umap_args = run_umap(data, group="group", annotation_cols=[])
umap_components = umap_result["umap"]
umap_components

# %% [markdown]
# # Embedding Plot (Static)

# %% [markdown]
# Acore function has defaults for the result type
# - the default size reflects in the width and height standards of journals
# - the axis titles and the group column returned by acore can be passed on directly
# - the loadings are optional and drawn as arrows (a biplot). Their length is scaled to the
#   range of the samples, which can be changed using `loading_factor`.

# %%
help(get_embedding_plot_static)

# %%
static_fig = get_embedding_plot_static(
    components, top_n_loadings=3, loadings=loadings, title="PCA", **pca_args
)
print(
    f"Static figure size (inches based on DPI {DEFAULT_DPI}):"
    f" {static_fig.get_size_inches()}"
)

# %% [markdown]
# The same function plots the UMAP embedding, here with custom colors.

# %%
static_fig = get_embedding_plot_static(
    umap_components,
    title="UMAP",
    colors=["pink", "orange", "teal"],
    **umap_args,
)

# %% [markdown]
# ## Manual calling of matplotlib (mpl) related function
# - data has to make sense for the plot, here the acore output is used as it is
# - loadings are not scaled, so they are multiplied by hand to be visible

# %%
help(get_embedding_plot_mpl)

# %%
_loadings = loadings.assign(x=loadings["x"] * 25, y=loadings["y"] * 25)
static_fig = get_embedding_plot_mpl(
    data=components,
    x="x",
    y="y",
    group="group",
    loadings=_loadings.head(3),
    title="PCA manual",
    x_title="PC1",
    y_title="PC2",
    width=700,
    height=500,
    # colors of colormap
    colors={"Sweden": "C0", "Magdeburg": "C1", "Kiel": "C2", "Berlin": "C3"},
)
print(
    f"Static figure size (inches based on DPI {DEFAULT_DPI}):"
    f" {static_fig.get_size_inches()}"
)

# %% [markdown]
# # Embedding Plot (Interactive)

# %% [markdown]
# Acore function has defaults for the result type
# - all columns besides `x`, `y` and `group` are shown when hovering, here `sample`
# - hovering over a loading shows its value

# %%
help(get_embedding_plot_interactive)

# %%
interactive_fig = get_embedding_plot_interactive(
    components,
    top_n_loadings=3,
    loadings=loadings,
    title="PCA",
    width=790,
    height=600,
    **pca_args,
)
interactive_fig

# %%
interactive_fig = get_embedding_plot_interactive(
    umap_components, title="UMAP", width=790, height=600, **umap_args
)
interactive_fig

# %% [markdown]
# ## Manual calling of plotly related function
# - data has to make sense for the plot, here the acore output is used as it is
# - additional columns can be added when hovering using `hovering_cols`

# %%
help(get_embedding_plot_plotly)

# %%
interactive_fig = get_embedding_plot_plotly(
    components,
    x="x",
    y="y",
    group="group",
    loadings=loadings.assign(x=loadings["x"] * 25, y=loadings["y"] * 25).head(3),
    title="PCA manual",
    x_title="PC1",
    y_title="PC2",
    width=790,
    height=500,
    colors={
        "Sweden": "pink",
        "Magdeburg": "orange",
        "Kiel": "teal",
        "Berlin": "purple",
    },
)
print(
    f"Interactive figure size (pixels): {interactive_fig.layout.width} x {interactive_fig.layout.height}"
)
interactive_fig

# %%
