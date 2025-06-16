from vuecore.engines import register_builder, register_saver
from .scatter import build as build_scatter
from .saver import save

# Register the functions with the central dispatcher
register_builder(plot_type="scatter", engine="plotly", func=build_scatter)
register_saver(engine="plotly", func=save)
