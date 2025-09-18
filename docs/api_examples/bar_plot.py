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
# # Bar Plot
#
# ![VueCore logo][vuecore_logo]
#
# [![Open In Colab][colab_badge]][colab_link]
#
# [VueCore][vuecore_repo] is a Python package for creating interactive and static visualizations of multi-omics data.
# It is part of a broader ecosystem of tools—including [ACore][acore_repo] for data processing and [VueGen][vuegen_repo] for automated reporting—that together enable end-to-end workflows for omics analysis.
#
# This notebook demonstrates how to generate bar plots using plotting functions from VueCore. We showcase basic and advanced plot configurations, highlighting key customization options such as grouping, color mapping, text annotations, and export to multiple file formats.
#
# ## Notebook structure
#
# First, we will set up the work environment by installing the necessary packages and importing the required libraries. Next, we will create basic and advanced bar plots.
#
# 0. [Work environment setup](#0-work-environment-setup)
# 1. [Basic bar plot](#1-basic-bar-plot)
# 2. [Advanced bar plot](#2-advanced-bar-plot)
#
# ## Credits and Contributors
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

# Create a directory for outputs
output_dir = "./outputs"
os.makedirs(output_dir, exist_ok=True)

# %% [markdown]
# ### 0.2. Importing libraries

# %%
from pathlib import Path

import numpy as np
import pandas as pd

from vuecore.plots.basic.bar import create_bar_plot

# %% [markdown]
# ### 0.3. Create sample data
# We create a synthetic dataset representing the relative abundances of common bacterial genera across various environmental samples.

# %% tags=["hide-input"]
# Set a random seed for reproducibility of the synthetic data
np.random.seed(42)

# Sample types and bacterial genera
sample_types = ["Soil", "Freshwater", "Ocean", "Sediment", "Wastewater"]
genera = [
    "Pseudomonas",
    "Bacillus",
    "Escherichia",
    "Streptococcus",
    "Lactobacillus",
    "Bacteroides",
    "Clostridium",
    "Staphylococcus",
    "Enterobacter",
    "Klebsiella",
    "Salmonella",
    "Shigella",
    "Vibrio",
]


def make_sample(sample: str, genera: list[str]) -> list[dict]:
    """
    Generate synthetic microbial abundance data for a single sample.

    Parameters
    ----------
    sample : str
        The sample type (e.g., 'Soil', 'Ocean', etc).
    genera : list[str]
        List of all possible bacterial genera.

    Returns
    -------
    list[dict]
        A list of dictionaries, each containing: Sample name, Genus,
        Relative abundance, and Genera count.
    """
    # Randomly pick a subset of genera present in this sample
    selected = np.random.choice(
        genera, np.random.randint(5, len(genera) + 1), replace=False
    )

    # Generate random raw abundances (shifted by +0.1 to avoid zeros)
    raw = np.random.rand(len(selected)) + 0.1

    # Normalize abundances so they sum to exactly 100%
    abundances = (raw / raw.sum()) * 100

    # Count how many genera are present
    genera_count = len(selected)

    # Store results into list of dicts
    return [
        {
            "Sample": sample,
            "Genus": genus,
            "Relative_Abundance": abund,
            "Genera_Count": genera_count,
        }
        for genus, abund in zip(selected, abundances)
    ]


# Generate full dataset by combining all samples
abund_df = pd.DataFrame(
    [row for sample in sample_types for row in make_sample(sample, genera)]
)
abund_df.head()

# %% [markdown]
# ## 1. Basic Bar Plot
# A basic bar plot can be created by simply providing the `x` and `y` columns from the DataFrame,
# along with style options like `title`
# using [`create_bar_plot`](vuecore.plots.basic.bar.create_bar_plot).

# %%
# Create a df with unique samples and their genera counts
bar_plot_basic_df = abund_df.drop_duplicates(subset="Sample")[
    ["Sample", "Genera_Count"]
]

# Define output path for the basic png plot
file_path_basic_png = Path(output_dir) / "bar_plot_basic.png"

# Generate the basic bar plot
bar_plot_basic = create_bar_plot(
    data=bar_plot_basic_df,
    x="Sample",
    y="Genera_Count",
    title="Genera Count by Sample Type",
    file_path=file_path_basic_png,
)

bar_plot_basic.show()

# %% [markdown]
# ## 2. Advanced Bar Plot
# Here is an example of an advanced `stacked bar plot` with more descriptive parameters, including `color grouping`, `text annotations`, `hover tooltips`, and export to `HTML`.

# %%
# Define the output file path for the HTML plot
file_path_adv_html = Path(output_dir) / "bar_plot_advanced.html"

# Generate the advanced stacked bar plot
bar_plot_adv = create_bar_plot(
    data=abund_df,
    x="Sample",
    y="Relative_Abundance",
    color="Genus",
    barmode="stack",
    title="Taxonomic Profile of Environmental Samples",
    subtitle="Relative Abundance of Bacterial Genera",
    labels={
        "Sample": "Environmental Sample Type",
        "Relative_Abundance": "Relative Abundance (%)",
        "Genus": "Genus",
    },
    hover_name="Genus",
    hover_data=["Relative_Abundance"],
    opacity=0.9,
    file_path=file_path_adv_html,
)

bar_plot_adv.show()
