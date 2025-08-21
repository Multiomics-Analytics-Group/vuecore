from typing import Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict


class BoxConfig(BaseModel):
    """
    Pydantic model for validating and managing box plot configurations.

    This model serves as a curated API for the most relevant parameters
    for box plots, closely aligned with the `plotly.express.box` API
    (https://plotly.com/python-api-reference/generated/plotly.express.box.html).

    It includes key parameters for data mapping, styling, and layout. It ensures
    that user-provided configurations are type-safe and adhere to the expected
    structure. The plotting function handles parameters defined here, and also
    accepts additional Plotly keyword arguments, forwarding them to the
    appropriate `plotly.express.box` or `plotly.graph_objects.Figure` call.

    Attributes
    ----------
    -----Data Mapping-----
    x : Optional[str]
        Column for the x-axis values.
    y : Optional[str]
        Column for the y-axis values.
    color : Optional[str]
        Column to assign color to box plots.
    hover_name : Optional[str]
        Column to appear in bold in the hover tooltip.
    hover_data : List[str]
        Additional columns to display in the hover tooltip.
    facet_row : Optional[str]
        Column to create vertical subplots (facets).
    facet_col : Optional[str]
        Column to create horizontal subplots (facets).
    labels : Optional[Dict[str, str]]
        Dictionary to override column names for titles, legends, etc.
    color_discrete_map : Optional[Dict[str, str]]
        Specific color mappings for values in the `color` column.
    category_orders : Optional[Dict[str, List[str]]]
        Dictionary to specify the order of categorical values.
    -----Styling and Layout-----
    orientation: str
        Orientation of the box plots ('v' for vertical, 'h' for horizontal).
    boxmode : str
        Mode for grouping boxes ('group' or 'overlay').
    log_x : bool
        If True, the x-axis is log-scaled.
    log_y : bool
        If True, the y-axis is log-scaled.
    range_x : Optional[List[float]]
        Range for the x-axis, e.g., [0, 100].
    range_y : Optional[List[float]]
        Range for the y-axis, e.g., [0, 100].
    notched : bool
        If True, boxes are drawn with notches.
    points : str
        Method to display sample points ('outliers', 'all', 'suspectedoutliers', False).
    title : str
        The main title of the plot.
    x_title : Optional[str]
        Custom title for the x-axis.
    y_title : Optional[str]
        Custom title for the y-axis.
    subtitle : Optional[str]
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
    x: Optional[str] = Field(None, description="Column for x-axis values.")
    y: Optional[str] = Field(None, description="Column for y-axis values.")
    color: Optional[str] = Field(None, description="Column to assign color to boxes.")
    hover_name: Optional[str] = Field(
        None, description="Column for bold text in hover tooltip."
    )
    hover_data: List[str] = Field(
        [], description="Additional columns for the hover tooltip."
    )
    facet_row: Optional[str] = Field(
        None, description="Column to create vertical subplots."
    )
    facet_col: Optional[str] = Field(
        None, description="Column to create horizontal subplots."
    )
    labels: Optional[Dict[str, str]] = Field(
        None, description="Override column names in the plot."
    )
    color_discrete_map: Optional[Dict[str, str]] = Field(
        None, description="Map values to specific colors."
    )
    category_orders: Optional[Dict[str, List[str]]] = Field(
        None, description="Dictionary to specify the order of categorical values."
    )

    # Styling and Layout
    orientation: Optional[str] = Field(
        None,
        description="Orientation of the box plots ('v' for vertical, 'h' for horizontal).",
    )
    boxmode: str = Field("group", description="Mode for grouping boxes.")
    log_x: bool = Field(False, description="If True, use a logarithmic x-axis.")
    log_y: bool = Field(False, description="If True, use a logarithmic y-axis.")
    range_x: Optional[List[float]] = Field(
        None, description="Range for the x-axis, e.g., [0, 100]."
    )
    range_y: Optional[List[float]] = Field(
        None, description="Range for the y-axis, e.g., [0, 100]."
    )
    notched: bool = Field(False, description="If True, boxes are drawn with notches.")
    points: str = Field(
        "outliers",
        description="Method to display sample points ('outliers', 'all', 'suspectedoutliers', False).",
    )
    title: str = Field("Box Plot", description="The main title of the plot.")
    x_title: Optional[str] = Field(None, description="Custom title for the x-axis.")
    y_title: Optional[str] = Field(None, description="Custom title for the y-axis.")
    subtitle: Optional[str] = Field(None, description="The subtitle of the plot.")
    template: str = Field("plotly_white", description="Plotly template for styling.")
    width: Optional[int] = Field(800, description="Width of the plot in pixels.")
    height: Optional[int] = Field(600, description="Height of the plot in pixels.")
