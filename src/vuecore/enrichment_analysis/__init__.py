"""
Focus on returning a single comparsion using `get_enrichment_plot`.

- should the vuecore interface be combined?

"""

from .interactive import (
    get_enrichment_plot,
    get_scatterplot,
)
from .static import get_enrichment_plot_static

__all__ = [
    "get_scatterplot",
    "get_enrichment_plot",
    "get_enrichment_plot_static",
]
