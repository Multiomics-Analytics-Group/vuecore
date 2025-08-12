from typing import Any

import pandas as pd

from vuecore import EngineType
from vuecore.engines import get_builder, get_saver
from vuecore.schemas.basic.line import LineConfig


def create_line_plot(
    data: pd.DataFrame,
    engine: EngineType = EngineType.PLOTLY,
    file_path: str = None,
    **kwargs,
) -> Any:
    """
    Creates, styles, and optionally saves a line plot using the specified engine.

    Parameters
    ----------
    data : pd.DataFrame
        The DataFrame containing the data to be plotted.
    engine : EngineType, optional
        The plotting engine to use for rendering the plot. Defaults to `EngineType.PLOTLY`.
    file_path : str, optional
        If provided, the path where the final plot will be saved. The file format
        is automatically inferred from the file extension (e.g., '.html', '.png').
        By default None.
    **kwargs
        Keyword arguments for plot configuration. These are validated against
        the `LineConfig` model. See `schemas.basic.line.LineConfig`
        for all available options.

    Returns
    -------
    Any
        The final plot object returned by the selected engine.
        For Plotly, this will be a `plotly.graph_objects.Figure`.
        For Matplotlib, a `matplotlib.figure.Figure`, etc.

    Raises
    ------
    pydantic.ValidationError
        If the provided kwargs do not match the `LineConfig` schema.
    ValueError
        If columns specified in the configuration do not exist in the DataFrame.

    Examples
    --------
    >>> import pandas as pd
    >>> data = {
    ...     "day": [1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
    ...     "value": [10, 12, 15, 11, 13, 20, 22, 19, 24, 25],
    ...     "value_error": [1, 1.2, 0.9, 1.5, 1.1, 2, 1.8, 2.2, 1.5, 2.5],
    ...     "experiment": ["A", "A", "A", "A", "A", "B", "B", "B", "B", "B"],
    ...     "condition": ["Control", "Control", "Treatment", "Treatment", "Treatment",
    ...                   "Control", "Control", "Treatment", "Treatment", "Treatment"],
    ...     "point_id": [f"A-{i}" for i in range(5)] + [f"B-{i}" for i in range(5)],
    ... }
    >>> sample_line_df = pd.DataFrame(data)
    >>>
    >>> # Create a basic line plot
    >>> fig_basic = create_line_plot(
    ...     data=sample_line_df,
    ...     x="day",
    ...     y="value",
    ...     color="experiment",
    ... )
    >>>
    >>> # Create an advanced line plot and save it to HTML
    >>> fig_advanced = create_line_plot(
    ...     data=sample_line_df,
    ...     x="day",
    ...     y="value",
    ...     color="experiment",
    ...     line_dash="condition",
    ...     error_y="value_error",
    ...     hover_name="point_id",
    ...     title="Experiment Value Over Time",
    ...     labels={"day": "Day of Trial", "value": "Measured Metric"},
    ...     color_discrete_map={"A": "#636EFA", "B": "#EF553B"},
    ...     line_dash_map={"Control": "solid", "Treatment": "dot"},
    ...     markers=True,
    ...     line_shape="spline",
    ...     file_path="my_advanced_line_plot.html"
    ... )
    """
    # 1. Validate configuration using Pydantic
    config = LineConfig(**kwargs)

    # 2. Get the correct builder function from the registry
    builder_func = get_builder(plot_type="line", engine=engine)

    # 3. Build the figure object (the API doesn't know or care what type it is)
    figure = builder_func(data, config)

    # 4. Save the plot using the correct saver
    if file_path:
        saver_func = get_saver(engine=engine)
        saver_func(figure, file_path)

    return figure
