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
# # Line Plot
#
# ![VueCore logo][vuecore_logo]
#
# [![Open In Colab][colab_badge]][colab_link]
#
# [VueCore][vuecore_repo] is a Python package for creating interactive and static visualizations of multi-omics data.
# It is part of a broader ecosystem of tools—including [ACore][acore_repo] for data processing and [VueGen][vuegen_repo] for automated reporting—that together enable end-to-end workflows for omics analysis.
#
# This notebook demonstrates how to generate line plots using plotting functions from VueCore. We showcase basic and
# advanced plot configurations, highlighting key customization options such as grouping, color mapping, text annotations, and export to multiple file formats.
#
# ## Notebook structure
#
# First, we will set up the work environment by installing the necessary packages and importing the required libraries. Next, we will create basic and advanced line plots.
#
# 0. [Work environment setup](#0-work-environment-setup)
# 1. [Basic line plot](#1-basic-line-plot)
# 2. [Advanced line plot](#2-advanced-line-plot)
#
# ## Credits and Contributors
# - This notebook was created by Sebastián Ayala-Ruano under the supervision of Henry Webel and Alberto Santos, head of the [Multiomics Network Analytics Group (MoNA)][Mona] at the [Novo Nordisk Foundation Center for Biosustainability (DTU Biosustain)][Biosustain].
# - You can find more details about the project in this [GitHub repository][vuecore_repo].
#
# [colab_badge]: https://colab.research.google.com/assets/colab-badge.svg
# [colab_link]: https://colab.research.google.com/github/Multiomics-Analytics-Group/vuecore/blob/main/docs/api_examples/line_plot.ipynb
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
# To run this notebook locally, you should create a virtual environment
# with the required libraries. If you are running this notebook on Google
# Colab, everything should be set.

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

from vuecore.plots.basic.line import create_line_plot

# %% [markdown]
# ### 0.3. Create sample data
# We create a synthetic dataset showing measurements over five days for
# two experiments (A, B), each tested under Control and Treatment
# conditions, with associated measurement errors.

# %% tags=["hide-input"]
sample_df = pd.DataFrame(
    {
        "day": list(range(1, 6)) * 4,  # 5 days
        "experiment": ["A"] * 10 + ["B"] * 10,  # 2 experiments
        "condition": (["Control"] * 5 + ["Treatment"] * 5) * 2,  # 2 conditions
        "value": [
            11,  # A - Control
            13,  # A - Control
            15,  # A - Control
            17,  # A - Control
            18,  # A - Control
            10,  # A - Treatment
            12,  # A - Treatment
            14,  # A - Treatment
            15,  # A - Treatment
            16,  # A - Treatment
            19,  # B - Control
            20,  # B - Control
            21,  # B - Control
            22,  # B - Control
            23,  # B - Control
            20,  # B - Treatment
            22,  # B - Treatment
            21,  # B - Treatment
            23,  # B - Treatment
            22,  # B - Treatment
        ],
        "value_error": [
            1.0,
            1.2,
            0.9,
            1.1,
            1.0,
            1.3,
            1.0,
            1.2,
            1.4,
            1.1,
            2.0,
            1.8,
            2.1,
            1.5,
            2.3,
            1.7,
            2.0,
            1.8,
            2.1,
            2.2,
        ],
    }
)

sample_df.head()

# %% [markdown]
# ## 1. Basic Line Plot
# A basic line plot can be created by simply providing the `x`, `y`, and
# `color` columns from the DataFrame
# using [`create_line_plot`](vuecore.plots.basic.line.create_line_plot).

# %%
# Define output path for the basic png plot
file_path_basic_png = Path(output_dir) / "line_plot_basic.png"

# Generate the basic bar plot
line_plot_basic = create_line_plot(
    data=sample_df,
    x="day",
    y="value",
    color="experiment",
    line_dash="condition",
    file_path=file_path_basic_png,
)

line_plot_basic.show()

# %% [markdown]
# ## 2. Advanced Line Plot
# Here is an example of an advanced line plot with more descriptive
# parameters, including `error bars`, `line styles`, `markers`, and
# `custom colors`.

# %%
# Define output file path for the HTML plot
file_path_adv_html = Path(output_dir) / "line_plot_advanced.html"

# Generate advanced line plot
line_plot_adv = create_line_plot(
    data=sample_df,
    x="day",
    y="value",
    color="experiment",
    line_dash="condition",
    error_y="value_error",
    title="Experiment & Condition Trends",
    subtitle="Measurements over 5 days for two experiments (A, B) under Control and Treatment conditions.",
    labels={
        "day": "Day",
        "value": "Response",
        "condition": "Condition",
        "experiment": "Experiment",
    },
    color_discrete_map={"A": "#508AA8", "B": "#A8505E"},
    line_dash_map={"Control": "solid", "Treatment": "dot"},
    markers=True,
    line_shape="spline",
    file_path=file_path_adv_html,
)

line_plot_adv.show()
