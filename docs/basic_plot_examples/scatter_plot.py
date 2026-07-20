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

# Create a directory for outputs
output_dir = "./outputs"
os.makedirs(output_dir, exist_ok=True)

# %% [markdown]
# ### 0.2. Importing libraries

# %%
from pathlib import Path

import pandas as pd

from vuecore.plots.basic.scatter import create_scatter_plot

# %% [markdown]
# ### 0.3. Create sample data
# We create a synthetic dataset that contains simulated gene expression values, p-values, regulation status, and significance scores for 8 genes across two cell types.

# %% tags=["hide-input"]
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

# %% [markdown]
# ## 1. Basic Scatter Plot
# A basic scatter plot can be created by providing the `x` and `y` columns
# from the DataFrame, along with style options like `title`
# using [`create_scatter_plot`](vuecore.plots.basic.scatter.create_scatter_plot).

# %%
# Define output path for the basic png plot
file_path_basic_png = Path(output_dir) / "scatter_basic.png"

# Generate the basic scatter plot
scatter_plot_basic = create_scatter_plot(
    data=sample_df,
    x="gene_expression",
    y="log_p_value",
    title="Basic Gene Expression Scatter Plot",
    file_path=file_path_basic_png,
)

scatter_plot_basic.show()

# %% [markdown]
# ## 2. Advanced Scatter Plot
# An example of an advanced scatter plot that includes grouping by a categorical variable, color mapping, text annotations, and adding several styling options.

# %%
# Define output file path for the HTML plot
file_path_adv_html = Path(output_dir) / "scatter_advanced.html"

# Generate advanced line plot
scatter_plot_adv = create_scatter_plot(
    data=sample_df,
    x="gene_expression",
    y="log_p_value",
    color="regulation",
    size="significance_score",
    text="gene_name",
    title="Advanced Gene Expression Scatter Plot",
    subtitle="Visualizing Gene Expression with Regulation and Significance",
    labels={
        "gene_expression": "Log2 Fold Change",
        "log_p_value": "Log P-value",
        "regulation": "Regulation Status",
        "significance_score": "Significance Score",
        "gene_name": "Gene Name",
    },
    color_discrete_map={"Up": "#508AA8", "Down": "#A8505E", "None": "#838383"},
    opacity=0.8,
    marker_line_width=1,
    marker_line_color="darkgray",
    width=900,
    height=600,
    file_path=file_path_adv_html,
)

scatter_plot_adv.show()
