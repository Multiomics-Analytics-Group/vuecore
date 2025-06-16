from vuecore.engines import register_builder, register_saver
from vuecore import PlotType, EngineType

from .scatter import build as build_scatter
from .saver import save

# Register the functions with the central dispatcher
register_builder(
    plot_type=PlotType.SCATTER, engine=EngineType.PLOTLY, func=build_scatter
)
register_saver(engine=EngineType.PLOTLY, func=save)
