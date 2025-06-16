from typing import Callable, Any

# Registries to hold the functions from each backend
PLOT_BUILDERS = {}
PLOT_SAVERS = {}


def register_builder(plot_type: str, engine: str, func: Callable):
    """Registers a plot builder function for a given type and engine."""
    if engine not in PLOT_BUILDERS:
        PLOT_BUILDERS[engine] = {}
    PLOT_BUILDERS[engine][plot_type] = func


def register_saver(engine: str, func: Callable):
    """Registers a save function for a given engine."""
    PLOT_SAVERS[engine] = func


def get_builder(plot_type: str, engine: str) -> Callable:
    """Retrieves a plot builder function from the registry."""
    try:
        return PLOT_BUILDERS[engine][plot_type]
    except KeyError:
        raise ValueError(f"No '{plot_type}' builder found for engine '{engine}'")


def get_saver(engine: str) -> Callable:
    """Retrieves a save function from the registry."""
    try:
        return PLOT_SAVERS[engine]
    except KeyError:
        raise ValueError(f"No saver found for engine '{engine}'")


# Import the engine modules to trigger their registration
from . import plotly

# from . import matplotlib # This is where you'd add a new engine
