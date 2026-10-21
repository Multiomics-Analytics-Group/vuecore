"""2D plots of dimensionality reductions (PCA, t-SNE, UMAP) from acore.

All methods share the `TwoComponentSchema` of `acore.types.exploratory_analysis`;
PCA results can additionally show their loadings (`TwoLoadingsSchema`) as a biplot.
"""

from .interactive import get_embedding_plot as get_embedding_plot_interactive
from .interactive import get_embedding_plot_plotly
from .static import get_embedding_plot as get_embedding_plot_static
from .static import get_embedding_plot_mpl

__all__ = [
    "get_embedding_plot_interactive",
    "get_embedding_plot_mpl",
    "get_embedding_plot_plotly",
    "get_embedding_plot_static",
]
