# VueCore: Project Structure and Workflow

This file provides an overview of the directory structure and general workflow for VueCore.

## Directory Structure

VueCore is organized into several subpackages (a directory with an `__init__.py` file)
that serve to different purposes, including **user-facing API**, **plotting engines**, **data validation schemas**, and **general utilities**. Here is a brief overview of the main directories with files for the scatter plot example:

```
├── vuecore/                    # The main source code package
│   ├── __init__.py             # Package initialization
│   ├── constants.py            # Global constants and enums (e.g., plot types, engine types)
│   ├── engines/                # Plotting backends (e.g., Plotly, Matplotlib)
│   │   ├── __init__.py         # Manages engine registration and loading
│   │   └── plotly/
│   │       ├── __init__.py     # Registers Plotly engine
│   │       ├── saver.py        # Functions for saving plots
│   │       ├── theming.py      # Applies styles and themes
│   │       └── scatter.py      # Generates Plotly scatter plots from a DataFrame and schema
│   ├── plots/                  # User-facing API for creating plots
│   │   └── basic/
│   │       └── scatter.py      # User API for creating scatter plots
│   ├── schemas/                # Pydantic models for plot configuration validation
│   │   └── basic/
│   │       └── scatter.py      # Schema for scatter plot configuration
│   └── utils/                  # Shared helper functions
│   │   ├── __init__.py       
│       ├── statistics.py       # Data transformation and statistical functions
│       └── doc_utils.py        # Documentation utilities
├── tests/                      # Unit and integration tests
│   └── test_scatter.py         # Tests for the scatter plot functionality
└── docs/                       # Documentation scripts and plot examples 
    └── api_examples/
│   │   ├── scatter_plot.ipynb  # Notebook demonstrating how to create scatter plots 
        └── scatter_plot.py     # Script demonstrating how to create scatter plots 
```

## Plot Generation Workflow

The process for generating a plot in VueCore follows a clear, sequential path, ensuring data is validated and rendered efficiently:

1. **User Interaction:** A user calls the main entry-point function from the `plots/` directory, for example, `plots.basic.scatter.create_scatter_plot`. They provide the data and any optional keyword arguments to define the plot's appearance. This can be done from any **Python script** or **Jupyter Notebook**, such as the examples provided in the `docs/api_examples` folder.
2. **Configuration Validation:** The function uses a **Pydantic schema** from the `schemas/` directory to validate the user's input. This step ensures all parameters are correctly typed and configured.
3. **Engine Selection:** The validated **configuration**, along with the **data** and chosen **engine** (e.g., Plotly), is passed to the `create_plot` factory function. This function selects the correct plotting engine and its corresponding `build` function.
4. **Plot Generation:** The engine's `build` function handles the steps of creating a plot:

    * It runs any necessary **preprocessing steps** (e.g., calculating density for color mapping).
    * It calls the appropriate **plotting function** (e.g., `px.scatter`) to generate the initial figure.
    * It applies **theming and styling** by calling a specific function (e.g., `apply_scatter_theme`).
5. **Return and Save:** The `build_plot` utility returns a `plotly.graph_objects.Figure` object, which is passed to the **user-facing function**. If a `file_path` was provided, the plot is saved to the specified location

Here is a visual representation of the workflow:

```
User Calls API
       ▼
   `vuecore/plots/basic/scatter.py`
       │
       ▼ Validates configuration
   `vuecore/schemas/basic/scatter.py`
       │
       ▼ Calls engine-specific build function
   `vuecore/engines/plotly/scatter.py:build`
       │
       ▼ Delegates to generic plot builder
   `vuecore/engines/plotly/plot_builder.py:build_plot`
       ├───► Preprocessing (`scatter_preprocess`)
       └───► Theming (`apply_scatter_theme`)
       │
       ▼ Returns final plot object
   `plotly.graph_objects.Figure`
       │
       ▼ Saves the final plot
   `vuecore/engines/plotly/saver.py`
```

## Tasks to Add a New Plot

We created a [new plot PR template][new-plot-pr-template] with a checklist of all the steps to follow, which you can use with a query paramter by clicking [here][new-plot-pr-query-param].

[new-plot-pr-template]: https://github.com/Multiomics-Analytics-Group/vuecore/blob/main/.github/PULL_REQUEST_TEMPLATE/new_plot.md
[new-plot-pr-query-param]: https://github.com/Multiomics-Analytics-Group/vuecore/compare/main...my-branch?quick_pull=1&template=new_plot.md