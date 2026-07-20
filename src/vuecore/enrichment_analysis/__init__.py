"""
Focus on returning a single comparsion using `get_enrichment_plot`.

- should the vuecore interface be combined?

"""

from .interactive import (
    create_enrichment_plots_interactive,
    get_enrichment_plot,
    get_enrichment_plots,
    get_scatterplot,
)
from .static import get_enrichment_plots_static

__all__ = [
    "get_scatterplot",
    "get_enrichment_plot",
    "get_enrichment_plots",
    "create_enrichment_plots_interactive",
    "get_enrichment_plots_static",
]
