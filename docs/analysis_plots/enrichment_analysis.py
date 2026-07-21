# %% [markdown]
# # Enrichment Analysis Plots
#
# Loads an example file created using acore. Presents the current plotting functions for
# an enrichment analysis result. The functions are available in the [`vuecore.enrichment_analysis` module](vuecore.enrichment_analysis).
#
# ## Overview
# For both static and interactive versions of the plots:
# - show acore related function that checks the input for compatibility
#   ([`EnrichmentAnalysisSchema`](acore.types.EnrichmentAnalysisSchema)) and calls the
#   backend specific plotting function with the required parameters.
# - show manually calling the backend specific plotting function with the required
#   parameters. For these, the setup of the data is the responsibility of the user. The
#   function will not check for compatibility and accepts [`DataFrame`s](pandas.DataFrame)
#   with only the required columns for that plot.

# %% tags=["hide-output"]
# %pip install vuecore

# %%
import numpy as np
import pandas as pd

from vuecore.enrichment_analysis import (
    get_enrichment_plot_interactive,
    get_enrichment_plot_static,
)
from vuecore.enrichment_analysis.interactive import get_enrichment_plot_plotly
from vuecore.enrichment_analysis.static import get_enrichment_plot_mpl

# %% [markdown]
# # Load example data
# - compatible with the `EnrichmentAnalysisSchema` type in acore.types

# %%
fname = "../../tests/data/enrichment_analysis.csv"
enrichment_results = pd.read_csv(fname, index_col=0).reset_index(drop=True)
enrichment_results

# %% [markdown]
# ## Reduced dataset for manual plotting function calling
# For illustration we will create a reduced dataset for manual plotting function calling.
# - here we only have one comparison, but for illustration we keep the boilerplate code
#   (show code) it as if there were multiple comparisons. The user has to select one of
#   the available comparisons for plotting. Most importantly, each category of the `direction`
#   column will be plotted in a different color. The `foreground` column will be used to
#   scale the marker size.


# %%
sel_columns = [
    "terms",
    # "identifiers",
    "foreground",
    # "background",
    # "foreground_pop",
    # "background_pop",
    "pvalue",
    "padj",
    "rejected",
    "direction",
    # "comparison",
]
selected_comparison = "control~10 µm sulforaphane"
df = (
    enrichment_results.query(f"comparison == '{selected_comparison}' and rejected")[
        sel_columns
    ]
    .copy()
    .sort_values(by=["direction", "padj"], ascending=False)
    .reset_index(drop=True)
)
df["x"] = -np.log10(df["pvalue"])
df

# %% [markdown]
# # Scatter Plot (Static)

# %% [markdown]
# Acore function has defaults for the result type
# - the default size reflects in the width and height standards of journals

# %%
help(get_enrichment_plot_static)

# %%
static_fig = get_enrichment_plot_static(
    enrichment_results,
)
print(f"Static figure size (inches): {static_fig.get_size_inches()}")

# %% [markdown]
# which can be adjusted.

# %%
static_fig = get_enrichment_plot_static(
    enrichment_results,
    width=900,
    height=500,
)
static_fig.get_axes()[0].legend(title="Direction", loc="lower left")
print(f"Static figure size (inches): {static_fig.get_size_inches()}")

# %% [markdown]
# ## Manual calling of matplotlib (mpl) related function
# - data has to make sense for the plot
# - size and other details can be adjusted

# %%
help(get_enrichment_plot_mpl)

# %%
static_fig = get_enrichment_plot_mpl(
    df=df,
    comparison_key=selected_comparison,
    group="direction",
    width=900,
    height=500,
    title="Enrichment manual",
    colors={
        "upregulated in control": "pink",
        "upregulated in 10 µm sulforaphane": "orange",
    },
)
static_fig.get_axes()[0].legend(title="Direction", loc="lower left")
print(f"Static figure size (inches): {static_fig.get_size_inches()}")

# %% [markdown]
# # Scatter Plot (Interactive)

# %% [markdown]
# Acore function has defaults for the result type

# %%
help(get_enrichment_plot_interactive)

# %%
interactive_fig = get_enrichment_plot_interactive(
    enrichment_results, width=790, height=500
)
interactive_fig

# %% [markdown]
# ## Manual calling of plotly related function
# - data has to make sense for the plot

# %%
help(get_enrichment_plot_plotly)

# %%
interactive_fig = get_enrichment_plot_plotly(
    df,
    x="x",
    y="terms",
    group="direction",
    symbol="direction",
    size="foreground",
    title="Enrichment manual",
    x_title="-log10(pvalue)",
    y_title="Enriched terms",
    width=790,
    height=500,
    colors={
        "upregulated in control": "pink",
        "upregulated in 10um sulforaphane": "green",
    },
)
print(
    f"Interactive figure size (pixels): {interactive_fig.layout.width} x {interactive_fig.layout.height}"
)
# get rid of the left and right large margin
interactive_fig.update_layout(
    margin=dict(l=5, r=5),
)
interactive_fig

# %%
