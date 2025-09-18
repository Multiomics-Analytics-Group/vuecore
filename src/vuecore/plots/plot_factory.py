from typing import Any, Type
import pandas as pd
from vuecore import EngineType, PlotType
from vuecore.engines import get_builder, get_saver
from pydantic import BaseModel


def create_plot(
    data: pd.DataFrame,
    config: Type[BaseModel],
    plot_type: PlotType,
    engine: EngineType = EngineType.PLOTLY,
    file_path: str = None,
    **kwargs,
) -> Any:
    """
    Factory function to create, style, and optionally save plots.

    This function handles the common workflow for creating plots:
    1. Validate configuration using the provided Pydantic model
    2. Get the appropriate builder function from the engine registry
    3. Build the figure using the builder
    4. Optionally save the plot if a file path is provided

    Parameters
    ----------
    data : pd.DataFrame
        The DataFrame containing the data to be plotted.
    config : Type[BaseModel]
        The Pydantic config class for validation.
    plot_type : PlotType
        The plot type from the `PlotType` enum (e.g., PlotType.BAR, PlotType.BOX, etc).
    engine : EngineType, optional
        The plotting engine to use for rendering the plot.
        Defaults to `EngineType.PLOTLY`.
    file_path : str, optional
        If provided, the path where the final plot will be saved.
    **kwargs
        Keyword arguments for plot configuration.

    Returns
    -------
    Any
        The final plot object returned by the selected engine.
    """
    # 1. Validate configuration using Pydantic
    config = config(**kwargs)

    # 2. Get the correct builder function from the registry
    builder_func = get_builder(plot_type=plot_type, engine=engine)

    # 3. Build the figure object
    figure = builder_func(data, config)

    # 4. Save the plot using the correct saver function, if a file_path is provided
    if file_path:
        saver_func = get_saver(engine=engine)
        saver_func(figure, file_path)

    return figure
