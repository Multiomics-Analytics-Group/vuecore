from typing import Callable
from vuecore import PlotType, EngineType

# Registries to hold the functions from each backend
PLOT_BUILDERS = {}
PLOT_SAVERS = {}


def register_builder(plot_type: PlotType, engine: EngineType, func: Callable):
    """
    Registers a plot builder function for a given plot type and engine.

    This allows dynamic dispatch of plotting functions depending on the desired
    plot type (e.g., scatter, histogram) and backend engine (e.g., Plotly, Matplotlib).

    Parameters
    ----------
    plot_type : PlotType
        The type of plot (e.g., SCATTER).
    engine : EngineType
        The rendering engine (e.g., PLOTLY).
    func : Callable
        The plotting function to register for this type and engine.

    Returns
    -------
    None
    """
    if engine not in PLOT_BUILDERS:
        PLOT_BUILDERS[engine] = {}
    PLOT_BUILDERS[engine][plot_type] = func


def register_saver(engine: EngineType, func: Callable):
    """
    Registers a save function for a given engine.

    This allows saving plots using engine-specific logic (e.g., Plotly's `write_image`,
    Matplotlib's `savefig`, etc.).

    Parameters
    ----------
    engine : EngineType
        The rendering engine for which to register the saver function.
    func : Callable
        The saving function to use for this engine.

    Returns
    -------
    None
    """
    PLOT_SAVERS[engine] = func


def get_builder(plot_type: PlotType, engine: EngineType) -> Callable:
    """
    Retrieves a plot builder function from the registry.

    Looks up the plotting function based on the specified plot type and engine.

    Parameters
    ----------
    plot_type : PlotType
        The type of plot to retrieve.
    engine : EngineType
        The engine used to render the plot.

    Returns
    -------
    Callable
        The registered plotting function.

    Raises
    ------
    ValueError
        If no function is found for the given plot type and engine.
    """
    try:
        return PLOT_BUILDERS[engine][plot_type]
    except KeyError:
        raise ValueError(f"No '{plot_type}' builder found for engine '{engine}'")


def get_saver(engine: EngineType) -> Callable:
    """
    Retrieves a save function from the registry.

    Returns the function used to save plots for the specified engine.

    Parameters
    ----------
    engine : EngineType
        The engine for which the saving function should be retrieved.

    Returns
    -------
    Callable
        The registered saving function.

    Raises
    ------
    ValueError
        If no saver function is registered for the given engine.
    """
    try:
        return PLOT_SAVERS[engine]
    except KeyError:
        raise ValueError(f"No saver found for engine '{engine}'")
