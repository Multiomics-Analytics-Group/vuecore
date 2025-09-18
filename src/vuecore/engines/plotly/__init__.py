from vuecore.engines.registry import register_builder, register_saver
from vuecore import PlotType, EngineType

from .scatter import build as build_scatter
from .line import build as build_line
from .bar import build as build_bar
from .box import build as build_box
from .violin import build as build_violin
from .histogram import build as build_histogram
from .saver import save

# Import build_utils to ensure it's available
from . import plot_builder  # noqa: F401

# Register the functions with the central dispatcher
register_builder(
    plot_type=PlotType.SCATTER, engine=EngineType.PLOTLY, func=build_scatter
)
register_builder(plot_type=PlotType.LINE, engine=EngineType.PLOTLY, func=build_line)
register_builder(plot_type=PlotType.BAR, engine=EngineType.PLOTLY, func=build_bar)
register_builder(plot_type=PlotType.BOX, engine=EngineType.PLOTLY, func=build_box)
register_builder(plot_type=PlotType.VIOLIN, engine=EngineType.PLOTLY, func=build_violin)
register_builder(
    plot_type=PlotType.HISTOGRAM, engine=EngineType.PLOTLY, func=build_histogram
)

register_saver(engine=EngineType.PLOTLY, func=save)
