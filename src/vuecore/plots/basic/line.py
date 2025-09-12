from typing import Any

import pandas as pd

from vuecore import EngineType, PlotType
from vuecore.schemas.basic.line import LineConfig
from vuecore.plots.plot_factory import create_plot
from vuecore.utils.docs_utils import document_pydant_params


@document_pydant_params(LineConfig)
def create_line_plot(
    data: pd.DataFrame,
    engine: EngineType = EngineType.PLOTLY,
    file_path: str = None,
    **kwargs,
) -> Any:
    """
    Creates, styles, and optionally saves a line plot using the specified engine.

    This function serves as the main entry point for users to generate line plots.
    It validates the provided configuration against the `LineConfig` schema,
    retrieves the appropriate plotting builder and saver functions based on the
    selected engine, builds the plot, and optionally saves it to a file.

    Parameters
    ----------
    data : pd.DataFrame
        The DataFrame containing the data to be plotted. Each row represents
        an observation, and columns correspond to variables.
    engine : EngineType, optional
        The plotting engine to use for rendering the plot.
        Defaults to `EngineType.PLOTLY`.
    file_path : str, optional
        If provided, the path where the final plot will be saved.
        The file format is automatically inferred from the file extension
        (e.g., '.html', '.png', '.jpeg', '.svg'). Defaults to None, meaning
        the plot will not be saved.

    Returns
    -------
    Any
        The final plot object returned by the selected engine.
        For Plotly, this will be a `plotly.graph_objects.Figure`.
        For Matplotlib, a `matplotlib.figure.Figure`, etc.

    Raises
    ------
    pydantic.ValidationError
        If the provided keyword arguments do not conform to the `LineConfig` schema,
        e.g., a required parameter is missing or a value has an incorrect type.
    ValueError
        Raised by the plotting engine (e.g., Plotly Express) if a
        column specified in the configuration (e.g., 'x', 'y', 'color') is
        not found in the provided DataFrame.

    Examples
    --------
    For detailed examples and usage, please refer to the documentation:

    * **Jupyter Notebook:** `docs/api_examples/line_plot.ipynb` -
    https://vuecore.readthedocs.io/en/latest/api_examples/scatter_plot.html
    * **Python Script:** `docs/api_examples/line_plot.py`
    """
    return create_plot(
        data=data,
        config=LineConfig,
        plot_type=PlotType.LINE,
        engine=engine,
        file_path=file_path,
        **kwargs,
    )
