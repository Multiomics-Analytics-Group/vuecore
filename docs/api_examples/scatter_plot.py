"""
Title: Scatter Plot Examples using VueCore
Description:
    This script demonstrates how to generate scatter plots using VueCore — a Python package for creating
    interactive and static visualizations of multi-omics data. It is part of an ecosystem including ACore
    for data processing and VueGen for automated reporting.

    We showcase basic and advanced plot configurations, highlighting customization options such as grouping,
    color mapping, annotations, and export to multiple formats.

Script Structure:
    0. Work environment setup
    1. Basic scatter plot
    2. Advanced scatter plot

Authors:
    Sebastián Ayala-Ruano
Supervisors:
    Henry Webel, Alberto Santos (Multiomics Network Analytics Group, DTU Biosustain)

Institution:
    Multiomics Network Analytics Group (MoNA),
    Novo Nordisk Foundation Center for Biosustainability (DTU Biosustain)

Project Repository:
    https://github.com/Multiomics-Analytics-Group/vuecore

License:
    MIT License

Created: 2025-06-25
Last Updated: 2025-06-25
"""

# %%
# 0. Work environment setup
# 0.1. Installing libraries and creating global variables for platform and working directory
# To run this notebook locally, you should create a virtual environment with the required libraries.
# pip install vuecore

# 0.2. Importing libraries
import os
import pandas as pd
import plotly.io as pio
from vuecore.plots.basic.scatter import create_scatter_plot

# Set the Plotly renderer based on the environment, default to notebook, but you can change it
# to "browser" if you do not want to use jupyter widgets.
pio.renderers.default = "notebook"

# 0.3. Create a directory for outputs
output_dir = "./outputs"
os.makedirs(output_dir, exist_ok=True)

# %%
# 1. Basic Scatter Plot
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

# Define output path
file_path_png = os.path.join(output_dir, "scatter_basic.png")

# Generate basic plot
fig = create_scatter_plot(
    data=sample_df,
    x="gene_expression",
    y="log_p_value",
    file_path=file_path_png,
)

fig.show()

# %%
# 2. Advanced Scatter Plot
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
    title="Advanced Gene Expression Plot",
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
