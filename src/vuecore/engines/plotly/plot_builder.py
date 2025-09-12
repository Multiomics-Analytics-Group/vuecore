# vuecore/engines/plotly/plot_builder.py
from typing import Any, Optional, List, Callable
import pandas as pd
import plotly.graph_objects as go


def build_plot(
    data: pd.DataFrame,
    config: Any,
    px_function: Callable,
    theming_function: Callable,
    theming_params: List[str],
    preprocess: Optional[Callable] = None,
) -> go.Figure:
    """
    Base function to build Plotly figures with common patterns.

    The function follows these steps:
    1. Get all parameters from the config model
    2. Create the dictionary of arguments for the plot function
    3. Apply preprocessing
    4. Create the base figure
    5. Apply theme and additional styling

    Parameters
    ----------
    data : pd.DataFrame
        The DataFrame containing the plot data.
    config : Any
        The Pydantic model with all plot configurations.
    px_function : Callable
        The Plotly Express function to use (e.g., px.bar, px.scatter, etc).
    theming_function : Callable
        The theming function to apply to the figure.
    theming_params : List[str]
        List of parameter names handled by the theming function.
    preprocess : Callable, Optional
        Optional preprocessing function for special features.

    Returns
    -------
    go.Figure
        A styled Plotly figure object.
    """
    # Get all parameters from the config model
    all_config_params = config.model_dump()

    # Create the dictionary of arguments for the plot function
    plot_args = {
        k: v
        for k, v in all_config_params.items()
        if k not in theming_params and v is not None
    }

    # Apply preprocessing if provided
    if preprocess and callable(preprocess):
        data, plot_args = preprocess(data, plot_args, config)

    # Create the base figure
    fig = px_function(data, **plot_args)

    # Apply theme and additional styling
    fig = theming_function(fig, config)

    return fig
