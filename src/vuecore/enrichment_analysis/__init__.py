"""
Focus on returning a single comparsion using `get_enrichment_plot`.

- should the vuecore interface be combined?

"""

from .interactive import get_enrichment_plot as get_enrichment_plot_interactive
from .interactive import get_enrichment_plot_plotly
from .static import get_enrichment_plot as get_enrichment_plot_static
from .static import get_enrichment_plot_mpl

__all__ = [
    "get_enrichment_plot_interactive",
    "get_enrichment_plot_static",
    "get_enrichment_plot_plotly",
    "get_enrichment_plot_mpl",
]
