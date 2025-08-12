from typing import Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict


class LineConfig(BaseModel):
    """
    Pydantic model for validating and managing line plot configurations.

    This model serves as a curated API for the most relevant parameters
    for line plots, closely aligned with the `plotly.express.line` API
    (https://plotly.com/python-api-reference/generated/plotly.express.line.html).

    The model ensures user-provided configurations are type-safe. The plotting
    function intelligently handles parameters defined here, and also accepts
    additional Plotly keyword arguments, forwarding them to the appropriate
    `plotly.express.line` or `plotly.graph_objects.Figure` call.

    This model includes the most relevant parameters for data mapping, styling,
    and layout. It ensures that user-provided configurations are type-safe and
    adhere to the expected structure. The plotting function handles parameters
    defined here, and also accepts additional Plotly keyword arguments,
    forwarding them to the appropriate `plotly.express.line` or
    `plotly.graph_objects.Figure` call.

    Attributes
    ----------
    -----Data Mapping-----
    x : str
        Column for the x-axis values.
    y : str
        Column for the y-axis values.
    line_group : Optional[str]
        Column to group data into separate lines.
    color : Optional[str]
        Column to assign color to lines. Replaces 'group'.
    line_dash : Optional[str]
        Column to assign dash styles to lines.
    symbol : Optional[str]
        Column to assign symbols to markers.
    hover_name : Optional[str]
        Column to appear in bold in the hover tooltip.
    hover_data : Optional[List[str]]
        Additional columns to display in the hover tooltip.
    text : Optional[str]
        Column for adding text labels to markers.
    facet_row : Optional[str]
        Column to create vertical subplots (facets).
    facet_col : Optional[str]
        Column to create horizontal subplots (facets).
    error_x : Optional[str]
        Column for sizing x-axis error bars.
    error_y : Optional[str]
        Column for sizing y-axis error bars.
    labels : Optional[Dict[str, str]]
        Dictionary to override column names for titles, legends, etc.
    color_discrete_map : Optional[Dict[str, str]]
        Specific color mappings for values in the `color` column.
    line_dash_map : Optional[Dict[str, str]]
        Specific dash style mappings for values in the `line_dash` column.
    symbol_map : Optional[Dict[str, str]]
        Specific symbol mappings for values in the `symbol` column.
    -----Styling and Layout-----
    markers : bool
        If True, markers are drawn on the lines.
    log_x : bool
        If True, the x-axis is log-scaled.
    log_y : bool
        If True, the y-axis is log-scaled.
    range_x : Optional[List[float]]
        Range for the x-axis, e.g., [0, 100].
    range_y : Optional[List[float]]
        Range for the y-axis, e.g., [0, 100].
    line_shape : Optional[str]
        Determines the line shape ('linear', 'spline', 'hv', etc.).
    title : str
        The main title of the plot.
    subtitle : str
        The subtitle of the plot.
    template : str
        Plotly template for styling (e.g., 'plotly_white').
    width : int
        Width of the plot in pixels.
    height : int
        Height of the plot in pixels.
    """

    # General Configuration
    # Allow extra parameters to pass through to Plotly
    model_config = ConfigDict(extra="allow")

    # Data Mapping
    x: str = Field(..., description="Column for x-axis values.")
    y: str = Field(..., description="Column for y-axis values.")
    line_group: Optional[str] = Field(
        None, description="Column to group data into separate lines."
    )
    color: Optional[str] = Field(None, description="Column to assign color to lines.")
    line_dash: Optional[str] = Field(
        None, description="Column to assign dash styles to lines."
    )
    symbol: Optional[str] = Field(
        None, description="Column to assign symbols to markers."
    )
    hover_name: Optional[str] = Field(
        None, description="Column for bold text in hover tooltip."
    )
    hover_data: List[str] = Field(
        [], description="Additional columns for the hover tooltip."
    )
    text: Optional[str] = Field(None, description="Column for text labels on markers.")
    facet_row: Optional[str] = Field(
        None, description="Column to create vertical subplots."
    )
    facet_col: Optional[str] = Field(
        None, description="Column to create horizontal subplots."
    )
    error_x: Optional[str] = Field(None, description="Column for x-axis error bars.")
    error_y: Optional[str] = Field(None, description="Column for y-axis error bars.")
    labels: Optional[Dict[str, str]] = Field(
        None, description="Override column names in the plot."
    )
    color_discrete_map: Optional[Dict[str, str]] = Field(
        None, description="Map values to specific colors."
    )
    line_dash_map: Optional[Dict[str, str]] = Field(
        None, description="Map values to specific dash styles."
    )
    symbol_map: Optional[Dict[str, str]] = Field(
        None, description="Map values to specific symbols."
    )

    # Styling and Layout
    markers: bool = Field(False, description="If True, displays markers on the lines.")
    log_x: bool = Field(False, description="If True, use a logarithmic x-axis.")
    log_y: bool = Field(False, description="If True, use a logarithmic y-axis.")
    range_x: Optional[List[float]] = Field(
        None, description="Range for the x-axis, e.g., [0, 100]."
    )
    range_y: Optional[List[float]] = Field(
        None, description="Range for the y-axis, e.g., [0, 100]."
    )
    line_shape: Optional[str] = Field(
        "linear", description="Line shape (e.g., 'linear', 'spline')."
    )
    title: str = Field("Line Plot", description="The main title of the plot.")
    subtitle: Optional[str] = Field(None, description="The subtitle for the plot.")
    template: str = Field("plotly_white", description="Plotly template for styling.")
    width: int = Field(800, description="Width of the plot in pixels.")
    height: int = Field(600, description="Height of the plot in pixels.")
