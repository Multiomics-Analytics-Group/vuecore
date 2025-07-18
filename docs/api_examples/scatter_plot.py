# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.2
#   kernelspec:
#     display_name: vuecore-dev
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Scatter Plot
#
# ![VueCore logo][vuecore_logo]
#
# [![Open In Colab][colab_badge]][colab_link]
#
# [VueCore][vuecore_repo] is a Python package for creating interactive and static visualizations of multi-omics data.
# It is part of a broader ecosystem of tools—including [ACore][acore_repo] for data processing and [VueGen][vuegen_repo] for automated reporting—that together enable end-to-end workflows for omics analysis.
#
# This notebook demonstrates how to generate scatter plots using plotting functions from VueCore. We showcase basic and
# advanced plot configurations, highlighting key customization options such as grouping, color mapping, text annotations, and export
# to multiple file formats.
#
# ## Notebook structure
#
# First, we will set up the work environment by installing the necessary packages and importing the required libraries. Next, we will create
# basic and advanced scatter plots.
#
# 0. [Work environment setup](#0-work-environment-setup)
# 1. [Basic scatter plot](#1-basic-scatter-plot)
# 2. [Advanced scatter plot](#2-advanced-scatter-plot)
#
# ## Credits and Contributors
# - This notebook was created by Sebastián Ayala-Ruano under the supervision of Henry Webel and Alberto Santos, head of the [Multiomics Network Analytics Group (MoNA)][Mona] at the [Novo Nordisk Foundation Center for Biosustainability (DTU Biosustain)][Biosustain].
# - You can find more details about the project in this [GitHub repository][vuecore_repo].
#
# [colab_badge]: https://colab.research.google.com/assets/colab-badge.svg
# [colab_link]: https://colab.research.google.com/github/Multiomics-Analytics-Group/vuecore/blob/main/docs/api_examples/scatter_plot.ipynb
# [vuecore_logo]: https://raw.githubusercontent.com/Multiomics-Analytics-Group/vuecore/main/docs/images/logo/vuecore_logo.svg
# [Mona]: https://multiomics-analytics-group.github.io/
# [Biosustain]: https://www.biosustain.dtu.dk/
# [vuecore_repo]: https://github.com/Multiomics-Analytics-Group/vuecore
# [vuegen_repo]: https://github.com/Multiomics-Analytics-Group/vuegen
# [acore_repo]: https://github.com/Multiomics-Analytics-Group/acore

# %% [markdown]
# ## 0. Work environment setup

# %% [markdown]
# ### 0.1. Installing libraries and creating global variables for platform and working directory
#
# To run this notebook locally, you should create a virtual environment with the required libraries. If you are running this notebook on Google Colab, everything should be set.

# %% tags=["hide-output"]
# VueCore library
# %pip install vuecore

# %% tags=["hide-cell"]
import os

IN_COLAB = "COLAB_GPU" in os.environ

# %% tags=["hide-cell"]
# Create a directory for outputs
output_dir = "./outputs"
os.makedirs(output_dir, exist_ok=True)

# %% [markdown]
# ### 0.2. Importing libraries

# %%
# Imports
import pandas as pd
import plotly.io as pio

from vuecore.plots.basic.scatter import create_scatter_plot

# Set the Plotly renderer based on the environment
pio.renderers.default = "notebook"

# %% [markdown]
# ## 1. Basic Scatter Plot

# %%
# Created sample data
sample_df = pd.DataFrame(
    {
        "gene_expression": [1.2, 2.5, 3.1, 4.5, 5.2, 6.8, 3.9, 2.1],
        "log_p_value": [0.5, 1.5, 2.0, 3.5, 4.0, 5.5, 1.8, 0.9],
        "regulation": ["Up", "Up", "None", "Down", "Down", "Down", "None", "Up"],
        "significance_score": [10, 20, 5, 40, 55, 80, 15, 25],
        "gene_name": [
            "GENE_A",
            "GENE_B",
            "GENE_C",
            "GENE_D",
            "GENE_E",
            "GENE_F",
            "GENE_G",
            "GENE_H",
        ],
        "cell_type": ["A", "B", "A", "B", "A", "B", "A", "B"],
    }
)

sample_df

# %%
# Define output path
file_path_png = os.path.join(output_dir, "scatter_basic.png")

# Generate basic plot
fig = create_scatter_plot(
    data=sample_df,
    x="gene_expression",
    y="log_p_value",
    title="Basic Gene Expression Scatter Plot",
    file_path=file_path_png,
)

fig.show()

# %% [markdown]
# ## 2. Advanced Scatter Plot

# %%
# Define output path
file_path_adv_html = os.path.join(output_dir, "scatter_advanced.html")

# Generate advanced plot
fig_advanced = create_scatter_plot(
    data=sample_df,
    x="gene_expression",
    y="log_p_value",
    group="regulation",
    size="significance_score",
    text="gene_name",
    title="Advanced Gene Expression Scatter Plot",
    x_title="Log2 Fold Change",
    y_title="-Log10(P-value)",
    colors={"Up": "#FF5733", "Down": "#3380FF", "None": "#33FF57"},
    marker_opacity=0.8,
    marker_line_width=1,
    marker_line_color="darkgray",
    width=900,
    height=600,
    file_path=file_path_adv_html,
)

fig_advanced.show()
