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
# # Histogram Plot
#
# ![VueCore logo][vuecore_logo]
#
# [![Open In Colab][colab_badge]][colab_link]
#
# [VueCore][vuecore_repo] is a Python package for creating interactive and static visualizations of multi-omics data.
# It is part of a broader ecosystem of tools—including [ACore][acore_repo] for data processing and [VueGen][vuegen_repo] for automated reporting—that together enable end-to-end workflows for omics analysis.
#
# This notebook demonstrates how to generate histogram plots using plotting functions from VueCore. We showcase basic and advanced plot configurations, highlighting key customization options such as grouping, color mapping, text annotations, and export to multiple file formats.
#
# ## Notebook structure
#
# First, we will set up the work environment by installing the necessary packages and importing the required libraries. Next, we will create basic and advanced histogram plots.
#
# 0. [Work environment setup](#0-work-environment-setup)
# 1. [Basic histogram plot](#1-basic-histogram-plot)
# 2. [Advanced histogram plot](#2-advanced-histogram-plot)
#
# ## Credits and Contributors
#
# - This notebook was created by Sebastián Ayala-Ruano under the supervision of Henry Webel and Alberto Santos, head of the [Multiomics Network Analytics Group (MoNA)][Mona] at the [Novo Nordisk Foundation Center for Biosustainability (DTU Biosustain)][Biosustain].
# - You can find more details about the project in this [GitHub repository][vuecore_repo].
#
# [colab_badge]: https://colab.research.google.com/assets/colab-badge.svg
# [colab_link]: https://colab.research.google.com/github/Multiomics-Analytics-Group/vuecore/blob/main/docs/api_examples/bar_plot.ipynb
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
from pathlib import Path

import numpy as np
import pandas as pd

from vuecore.plots.basic.histogram import create_histogram_plot

# %% [markdown]
# ### 0.3. Create sample data
# We create a synthetic dataset simulating gene expression data across two experimental
# conditions to demonstrate how histograms can visualize data distribution.

# %% tags=["hide-input"]
# Set a random seed for reproducibility of the synthetic data
np.random.seed(42)

# Define parameters for synthetic gene expression data
num_genes = 1000
conditions = ["Control", "Treated"]
gene_names = [f"Gene_{i}" for i in range(num_genes)]

# Simulate expression data with a slight shift in the "Treated" group
expression_values = np.concatenate(
    [
        np.random.normal(loc=10, scale=2, size=num_genes // 2),
        np.random.normal(loc=12, scale=2, size=num_genes // 2),
    ]
)
condition_values = np.concatenate(
    [["Control"] * (num_genes // 2), ["Treated"] * (num_genes // 2)]
)

# Create the DataFrame
gene_exp_df = pd.DataFrame(
    {
        "Gene_ID": gene_names,
        "Expression": expression_values,
        "Condition": condition_values,
    }
)

gene_exp_df.head()

# %% [markdown]
# ## 1. Basic Histogram Plot
# A basic histogram plot can be created by simply providing the `x` and `y` columns from the DataFrame,
# along with style options like `title`
# using [`create_histogram_plot`](vuecore.plots.basic.histogram.create_histogram_plot) .

# %%
# Define output file path for the PNG basic histogram
file_path_basic_hist_png = Path(output_dir) / "histogram_plot_basic.png"

# Generate the basic histogram plot
histogram_plot_basic = create_histogram_plot(
    data=gene_exp_df,
    x="Expression",
    title="Distribution of Gene Expression Levels",
    file_path=file_path_basic_hist_png,
)

histogram_plot_basic.show()

# %% [markdown]
# ## 2. Advanced Histogram Plot
# Here is an example of an advanced histogram plot with more descriptive parameters, including `color grouping`, `overlay barmode`, `probability density normalization`, `hover tooltips`, and export to `HTML`.

# %%
# Define the output file path for the advanced HTML histogram
file_path_adv_hist_html = Path(output_dir) / "histogram_plot_advanced.html"

# Generate the advanced histogram plot
histogram_plot_adv = create_histogram_plot(
    data=gene_exp_df,
    x="Expression",
    color="Condition",
    barmode="overlay",
    histnorm="probability density",
    title="Gene Expression Distribution by Treatment Condition",
    subtitle="Histogram with probability density normalized",
    labels={"Expression": "Gene Expression", "Condition": "Treatment Condition"},
    hover_data=["Gene_ID"],
    opacity=0.75,
    file_path=file_path_adv_hist_html,
)

histogram_plot_adv.show()
