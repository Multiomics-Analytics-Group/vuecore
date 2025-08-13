from typing import Any

import pandas as pd

from vuecore import EngineType
from vuecore.engines import get_builder, get_saver
from vuecore.schemas.basic.scatter import ScatterConfig


def create_scatter_plot(
    data: pd.DataFrame,
    engine: EngineType = EngineType.PLOTLY,
    file_path: str = None,
    **kwargs,
) -> Any:
    """
    Creates, styles, and optionally saves a scatter plot using the specified engine.

    Parameters
    ----------
    data : pd.DataFrame
        The DataFrame containing the data to be plotted.
    engine : EngineType, optional
        The plotting engine to use for rendering the plot. Defaults to `EngineType.PLOTLY`.
    file_path : str, optional
        If provided, the path where the final plot will be saved. The file format
        is automatically inferred from the file extension (e.g., '.html', '.png').
        By default None.
    **kwargs
        Keyword arguments for plot configuration. These are validated against
        the `ScatterConfig` model. See `schemas.relational.scatter.ScatterConfig`
        for all available options.

    Returns
    -------
    Any
        The final plot object returned by the selected engine.
        For Plotly, this will be a `plotly.graph_objects.Figure`.
        For Matplotlib, a `matplotlib.figure.Figure`, etc.

    Raises
    ------
    pydantic.ValidationError
        If the provided keyword arguments do not conform to the `ScatterConfig` schema,
        e.g. a required parameter is missing or a value has an incorrect type.
    ValueError
        Raised by the plotting engine if a column specified in the configuration is not
        found in the provided DataFrame.

    Examples
    --------
    For detailed examples and usage, please refer to the documentation:

    * **Jupyter Notebook:** `docs/api_examples/scatter_plot.ipynb` -
    https://vuecore.readthedocs.io/en/latest/api_examples/scatter_plot.html
    * **Python Script:** `docs/api_examples/scatter_plot.py` -
    https://github.com/Multiomics-Analytics-Group/vuecore/blob/main/docs/api_examples/scatter_plot.py
    """
    # 1. Validate configuration using Pydantic
    config = ScatterConfig(**kwargs)

    # 2. Get the correct builder function from the registry
    builder_func = get_builder(plot_type="scatter", engine=engine)

    # 3. Build the figure object (the API doesn't know or care what type it is)
    figure = builder_func(data, config)

    # 4. Save the plot using the correct saver
    if file_path:
        saver_func = get_saver(engine=engine)
        saver_func(figure, file_path)

    return figure
