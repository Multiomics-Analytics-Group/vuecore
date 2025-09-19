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
# # Box and Violin Plots
#
# ![VueCore logo][vuecore_logo]
#
# [![Open In Colab][colab_badge]][colab_link]
#
# [VueCore][vuecore_repo] is a Python package for creating interactive and static visualizations of multi-omics data.
# It is part of a broader ecosystem of tools—including [ACore][acore_repo] for data processing and [VueGen][vuegen_repo] for automated reporting—that together enable end-to-end workflows for omics analysis.
#
# This notebook demonstrates how to generate box and violin plots using plotting functions from VueCore. We showcase basic and advanced plot configurations, highlighting key customization options such as grouping, color mapping, text annotations, and export to multiple file formats.
#
# ## Notebook structure
#
# First, we will set up the work environment by installing the necessary packages and importing the required libraries. Next, we will create basic and advanced box plots.
#
# 0. [Work environment setup](#0-work-environment-setup)
# 1. [Basic box plot](#1-basic-box-plot)
# 2. [Basic violin plot](#2-basic-violin-plot)
# 3. [Advanced box plot](#3-advanced-box-plot)
# 4. [Advanced violin plot](#3-advanced-violin-plot)
#
# ## Credits and Contributors
# - This notebook was created by Sebastián Ayala-Ruano under the supervision of Henry Webel and Alberto Santos, head of the [Multiomics Network Analytics Group (MoNA)][Mona] at the [Novo Nordisk Foundation Center for Biosustainability (DTU Biosustain)][Biosustain].
# - You can find more details about the project in this [GitHub repository][vuecore_repo].
#
# [colab_badge]: https://colab.research.google.com/assets/colab-badge.svg
# [colab_link]: https://colab.research.google.com/github/Multiomics-Analytics-Group/vuecore/blob/main/docs/api_examples/box_plot.ipynb
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

import numpy as np
import pandas as pd

from vuecore.plots.basic.box import create_box_plot
from vuecore.plots.basic.violin import create_violin_plot

# %% [markdown]
# ### 0.3. Create sample data
# We create a synthetic dataset simulating gene expression levels across different
# patient samples and treatment conditions, with each data point representing a
# unique gene's expression level under a specific treatment for a particular patient.

# %% tags=["hide-input"]
# Set a random seed for reproducibility of the synthetic data
np.random.seed(42)

# Parameters
num_samples = 200
sample_groups = ["Patient A", "Patient B", "Patient C", "Patient D"]
treatments = ["Control", "Treated"]

# Sample metadata
sample_ids = np.random.choice(sample_groups, size=num_samples)
treatment_assignments = np.random.choice(treatments, size=num_samples)
gene_ids = [f"Gene_{g}" for g in np.random.randint(1, 1500, size=num_samples)]

# Base expression values
base_expr = np.random.normal(loc=100, scale=35, size=num_samples)

# Treatment effect simulation
treatment_effect = np.where(
    treatment_assignments == "Treated",
    np.random.normal(loc=50, scale=30, size=num_samples),
    0,
)

# Small random per-gene offset for extra variability
gene_offset = np.random.normal(loc=0, scale=20, size=num_samples)

# Final expression
expr = base_expr + treatment_effect + gene_offset

# Construct DataFrame
gene_exp_df = pd.DataFrame(
    {
        "Sample_ID": sample_ids,
        "Treatment": treatment_assignments,
        "Gene_ID": gene_ids,
        "Expression": expr,
    }
)
gene_exp_df

# %% [markdown]
# ## 1. Basic Box Plot
# A basic box plot can be created by simply providing the `x` and `y` columns from the DataFrame,
# along with style options like `title`
# using [`create_box_plot`](vuecore.plots.basic.box.create_box_plot).

# %%
# Define output file path for the PNG basic box plot
file_path_basic_box_png = Path(output_dir) / "box_plot_basic.png"

# Generate the basic box plot
box_plot_basic = create_box_plot(
    data=gene_exp_df,
    x="Treatment",
    y="Expression",
    title="Gene Expression Levels by Treatment",
    file_path=file_path_basic_box_png,
)

box_plot_basic.show()

# %% [markdown]
# ## 2. Basic Violin Plot
# A basic violin plot can be created by simply providing the `x` and `y` columns from the DataFrame,
# along with style options like `title`
# using [`create_violin_plot`](vuecore.plots.basic.violin.create_violin_plot) .

# %%
# Define output file path for the PNG basic violin plot
file_path_basic_violin_png = Path(output_dir) / "violin_plot_basic.png"

# Generate the basic violin plot
violin_plot_basic = create_violin_plot(
    data=gene_exp_df,
    x="Treatment",
    y="Expression",
    title="Gene Expression Levels by Treatment",
    file_path=file_path_basic_violin_png,
)

violin_plot_basic.show()

# %% [markdown]
# ## 3. Advanced Box Plot
# Here is an example of an advanced box plot with more descriptive parameters, including `color and box grouping`, `text annotations`, `hover tooltips`, and export to `HTML`.

# %%
# Define the output file path for the advanced HTML box plot
file_path_adv_box_html = Path(output_dir) / "box_plot_advanced.html"

# Generate the advanced box plot
box_plot_adv = create_box_plot(
    data=gene_exp_df,
    x="Treatment",
    y="Expression",
    color="Sample_ID",
    boxmode="group",
    notched=True,
    title="Gene Expression Levels with Control and Treatment Condition",
    subtitle="Distribution of gene expression across different treatments and patient samples",
    labels={
        "Treatment": "Treatment",
        "Expression": "Gene Expression",
        "Sample_ID": "Patient Sample ID",
    },
    color_discrete_map={
        "Patient A": "#508AA8",
        "Patient B": "#A8505E",
        "Patient C": "#86BF84",
        "Patient D": "#A776AF",
    },
    category_orders={"Sample_ID": ["Patient A", "Patient B", "Patient C", "Patient D"]},
    hover_data=["Gene_ID"],
    file_path=file_path_adv_box_html,
)

box_plot_adv.show()

# %% [markdown]
# ## 4. Advanced Violin Plot
# Here is an example of an advanced violin plot with more descriptive parameters, including `color and box grouping`, `text annotations`, `hover tooltips`, and export to `HTML`.

# %%
# Define the output file path for the advanced HTML violin plot
file_path_adv_violin_html = Path(output_dir) / "violin_plot_advanced.html"

# Generate the advanced box plot
violin_plot_adv = create_violin_plot(
    data=gene_exp_df,
    x="Treatment",
    y="Expression",
    color="Sample_ID",
    violinmode="group",
    points="outliers",
    title="Gene Expression Levels with Control and Treatment Condition",
    subtitle="Distribution of gene expression across different treatments and patient samples",
    labels={
        "Treatment": "Treatment",
        "Expression": "Gene Expression",
        "Sample_ID": "Patient Sample ID",
    },
    color_discrete_map={
        "Patient A": "#508AA8",
        "Patient B": "#A8505E",
        "Patient C": "#86BF84",
        "Patient D": "#A776AF",
    },
    category_orders={"Sample_ID": ["Patient A", "Patient B", "Patient C", "Patient D"]},
    hover_data=["Gene_ID"],
    file_path=file_path_adv_violin_html,
)

violin_plot_adv.show()
