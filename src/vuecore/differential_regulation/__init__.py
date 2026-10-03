from .interactive import (
    get_differential_regulation_plot as get_differential_regulation_plot_interactive,
)
from .interactive import (
    get_volcano_plot_plotly,
)
from .static import (
    get_differential_regulation_plot as get_differential_regulation_plot_static,
)
from .static import (
    get_volcano_plot_mpl,
)

__all__ = [
    "get_differential_regulation_plot_interactive",
    "get_differential_regulation_plot_static",
    "get_volcano_plot_mpl",
    "get_volcano_plot_plotly",
]
