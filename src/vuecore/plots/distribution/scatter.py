import pandas as pd
import plotly.graph_objects as go

from vuecore.schemas.distribution.scatter import ScatterConfig

from vuecore.utils.validation import validate_columns_exist
from vuecore.engines import get_builder, get_saver
from vuecore import EngineType


def create_scatter_plot(
    data: pd.DataFrame,
    engine: EngineType = EngineType.PLOTLY,
    file_path: str = None,
    **kwargs,
) -> go.Figure:
    """
    Creates, styles, and optionally saves a scatter plot using the specified engine.

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
        the `ScatterConfig` model. See `schemas.relational.scatter.ScatterConfig`
        for all available options.

    Returns
    -------
    go.Figure
        The final, styled `plotly.graph_objects.Figure` object.

    Raises
    ------
    pydantic.ValidationError
        If the provided kwargs do not match the `ScatterConfig` schema.
    ValueError
        If columns specified in the configuration do not exist in the DataFrame.

    Examples
    --------
    >>> import pandas as pd
    >>> sample_df = pd.DataFrame({
    ...     'gene_expression': [1.2, 2.5, 3.1, 4.5, 5.2, 6.8],
    ...     'log_p_value': [0.5, 1.5, 2.0, 3.5, 4.0, 5.5],
    ...     'regulation': ['Up', 'Up', 'None', 'Down', 'Down', 'Down'],
    ...     'significance_score': [10, 20, 5, 40, 55, 80],
    ...     'gene_name': ['GENE_A', 'GENE_B', 'GENE_C', 'GENE_D', 'GENE_E', 'GENE_F']
    ... })
    >>>
    >>> # Create a simple scatter plot and save it to HTML
    >>> fig = create_scatter_plot(
    ...     data=sample_df,
    ...     x='gene_expression',
    ...     y='log_p_value',
    ...     group='regulation',
    ...     size='significance_score',
    ...     text='gene_name',
    ...     title="Gene Expression vs. Significance",
    ...     x_title="Log2 Fold Change",
    ...     y_title="-Log10(P-value)",
    ...     colors={'Up': '#d62728', 'Down': '#1f77b4', 'None': '#7f7f7f'},
    ...     file_path="my_scatter_plot.html"
    ... )
    >>>
    >>> # The returned `fig` object can be displayed in a notebook or further modified
    >>> # fig.show()
    """
    # 1. Validate configuration using Pydantic
    config = ScatterConfig(**kwargs)

    # 2. Perform data-specific validation
    required_cols = [
        col
        for col in [
            config.x,
            config.y,
            config.group,
            config.size,
            config.symbol,
            config.text,
        ]
        if col is not None
    ]
    validate_columns_exist(data, required_cols)

    # 2. Get the correct builder function from the registry
    builder_func = get_builder(plot_type="scatter", engine=engine)

    # 3. Build the figure object (the API doesn't know or care what type it is)
    figure = builder_func(data, config)

    # 4. Save the plot using the correct saver
    if file_path:
        saver_func = get_saver(engine=engine)
        saver_func(figure, file_path)

    return figure
