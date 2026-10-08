# %% [markdown]
# # Differential Regulation Plots
#
# Loads an example file created using acore `0.3.2`. Presents the current plotting functions for
# a differential regulation (ANOVA) result as a volcano plot. The functions are available
# in the [`vuecore.differential_regulation` module](vuecore.differential_regulation).
#
# ## Overview
# For both static and interactive versions of the plots:
# - show acore related function that checks the input for compatibility
#   ([`AnovaSchema`](acore.types.AnovaSchema) or
#   [`AnovaSchemaMultiGroup`](acore.types.AnovaSchemaMultiGroup)) and calls the
#   backend specific plotting function with the required parameters.
# - show manually calling the backend specific plotting function with the required
#   parameters. For these, the setup of the data is the responsibility of the user. The
#   function will not check for compatibility and accepts [`DataFrame`s](pandas.DataFrame)
#   with only the required columns for that plot.

# %% tags=["hide-output"]
# %pip install vuecore

# %% tags=["hide-input"]
from pathlib import Path

import pandas as pd

from vuecore.differential_regulation import (
    get_differential_regulation_plot_interactive,
    get_differential_regulation_plot_static,
)
from vuecore.differential_regulation.common import assign_regulation, label_top_n
from vuecore.differential_regulation.interactive import get_volcano_plot_plotly

# DEFAULT_DPI should move
from vuecore.differential_regulation.static import (
    DEFAULT_DPI,
    get_volcano_plot_mpl,
)

# %% [markdown]
# # Load example data
# - compatible with the `AnovaSchemaMultiGroup` type in acore.types
# - feature identifiers are in the index
# - several comparisons are in the table (`group1` and `group2` columns)

# %% tags=["hide-input"]
fname = "../../tests/data/differential_analysis.csv"
fname_url = (
    "https://raw.githubusercontent.com/Multiomics-Analytics-Group/"
    "vuecore/refs/heads/main/tests/data/differential_analysis.csv"
)

if not Path(fname).exists():
    fname = fname_url
diff_reg = pd.read_csv(fname, index_col=0).sort_index()
diff_reg

# %% [markdown]
# Available comparisons:

# %% tags=["hide-input"]
diff_reg[["group1", "group2", "posthoc comparison"]].drop_duplicates().reset_index(
    drop=True
)

# %%
view = diff_reg.filter(like="posthoc").head().T
view

# %%
# columns not in view
diff_reg[diff_reg.columns.difference(view.index)].head().T

# %% [markdown]
# ## Reduced dataset for manual plotting function calling
# For illustration we will create a reduced dataset for manual plotting function calling.
# - the user has to select one of the available comparisons for plotting.
# - each category of the `regulation` column will be plotted in a different color.
# - the `label` column holds the text shown next to the dots, here for the features with
#   the smallest p-values.

# %% tags=["hide-input"]
group1, group2 = "WT", "rapZE227Stop"
selected_comparison = f"{group1}~{group2}"
df = diff_reg.query("group1 == @group1 and group2 == @group2")[
    ["log2FC", "FC", "-log10 posthoc pvalue", "posthoc pvalue adj", "posthoc rejected"]
].copy()
df["regulation"] = assign_regulation(
    diff_reg.loc[df.index].query("group1 == @group1 and group2 == @group2"),
    group1,
    group2,
    col_rejected="posthoc rejected",
)
df["label"] = label_top_n(df, "posthoc pvalue adj", top_n=5)
df

# %% [markdown]
# # Volcano Plot (Static)

# %% [markdown]
# Acore function has defaults for the result type
# - the default size reflects in the width and height standards of journals
# - as there are multiple comparisons, one has to be selected

# %%
help(get_differential_regulation_plot_static)

# %%
static_fig = get_differential_regulation_plot_static(
    diff_reg, comparison=selected_comparison
)
print(
    f"Static figure size (inches based on DPI {DEFAULT_DPI}):"
    f" {static_fig.get_size_inches()}"
)

# %% [markdown]
# which can be adjusted, e.g. the number of labelled features, size and colors.

# %%
static_fig = get_differential_regulation_plot_static(
    diff_reg,
    comparison=selected_comparison,
    top_n=5,
    width=900,
    height=500,
    colors=["pink", "orange"],
)
print(
    f"Static figure size (inches based on DPI {DEFAULT_DPI}):"
    f" {static_fig.get_size_inches()}"
)

# %% [markdown]
# ## Manual calling of matplotlib (mpl) related function
# - data has to make sense for the plot, uses the manually curated view `df`
# - size and other details can be adjusted

# %%
help(get_volcano_plot_mpl)

# %%
static_fig = get_volcano_plot_mpl(
    data=df,
    x="log2FC",
    y="-log10 posthoc pvalue",
    group="regulation",
    text="label",
    width=900,
    height=500,
    title="Volcano manual",
    colors={
        "not regulated": "lightgrey",
        f"upregulated in {group1}": "pink",
        f"upregulated in {group2}": "orange",
    },
)
print(
    f"Static figure size (inches based on DPI {DEFAULT_DPI}):"
    f" {static_fig.get_size_inches()}"
)

# %% [markdown]
# # Volcano Plot (Interactive)

# %% [markdown]
# Acore function has defaults for the result type

# %%
help(get_differential_regulation_plot_interactive)

# %%
interactive_fig = get_differential_regulation_plot_interactive(
    diff_reg, comparison=selected_comparison, width=790, height=500
)
interactive_fig

# %% [markdown]
# ## Manual calling of plotly related function
# - data has to make sense for the plot, uses the manually curated view `df`
# - the index is shown when hovering, additional columns can be added using
#   `hovering_cols`

# %%
help(get_volcano_plot_plotly)

# %%
interactive_fig = get_volcano_plot_plotly(
    df,
    x="log2FC",
    y="-log10 posthoc pvalue",
    group="regulation",
    text="label",
    hovering_cols=["posthoc pvalue adj", "FC"],
    title="Volcano manual",
    x_title="log2 fold change",
    y_title="-log10(p-value)",
    width=790,
    height=500,
    colors={
        "not regulated": "lightgrey",
        f"upregulated in {group1}": "pink",
        f"upregulated in {group2}": "green",
    },
)
print(
    f"Interactive figure size (pixels): {interactive_fig.layout.width} x {interactive_fig.layout.height}"
)
interactive_fig

# %%
