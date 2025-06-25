from vuecore.engines.registry import get_builder, get_saver

# Import the engine modules to trigger their registration
from . import plotly  # noqa: F401, E402

# from . import matplotlib # This is where you'd add a new engine

__all__ = ["get_builder", "get_saver"]
