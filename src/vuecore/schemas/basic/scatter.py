from typing import Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict, model_validator


class ScatterConfig(BaseModel):
    """
    Pydantic model for validating and managing scatter plot configurations.

    This model serves as a curated API for the most relevant parameters
    for scatter plots, closely aligned with the `plotly.express.scatter` API
    (https://plotly.com/python-api-reference/generated/plotly.express.scatter.html).

    This model includes the most relevant parameters for data mapping, styling,
    and layout. It ensures that user-provided configurations are type-safe and
    adhere to the expected structure. The plotting function handles parameters
    defined here, and also accepts additional Plotly keyword arguments,
    forwarding them to the appropriate `plotly.express.scatter` or
    `plotly.graph_objects.Figure` call.

    Attributes
    ---------
    -----Data Mapping-----
    x : str
        Column name for x-axis values.
    y : str
        Column name for y-axis values.
    color : Optional[str]
        Column to assign color to markers.
    symbol : Optional[str]
        Column to assign marker symbols.
    size : Optional[str]
        Column to determine marker size.
    hover_name : Optional[str]
        Column for bold text in hover tooltip.
    hover_data : List[str]
        Additional columns for hover tooltip.
    text : Optional[str]
        Column for text labels on markers.
    facet_row : Optional[str]
        Column for vertical facetting.
    facet_col : Optional[str]
        Column for horizontal facetting.
    error_x : Optional[str]
        Column for x-axis error bars.
    error_y : Optional[str]
        Column for y-axis error bars.
    labels : Optional[Dict[str, str]]
        Column name overrides for display.
    color_discrete_map : Optional[Dict[str, str]]
        Specific color mappings for color column values.
    symbol_map : Optional[Dict[str, str]]
        Specific symbol mappings for symbol column values.
    -----Styling and Layout-----
    opacity : float
        Marker opacity (0-1).
    size_max : int
        Maximum marker size.
    trendline : Optional[str]
        Trendline type (ols/lowess/rolling/expanding/ewm).
    trendline_options : Optional[Dict]
        Advanced options for trendlines.
    log_x : bool
        Enable logarithmic x-axis.
    log_y : bool
        Enable logarithmic y-axis.
    range_x : Optional[List[float]]
        Manual x-axis range [min, max].
    range_y : Optional[List[float]]
        Manual y-axis range [min, max].
    title : str
        Main plot title.
    subtitle : Optional[str]
        Plot subtitle.
    template : str
        Plotly visual theme/template.
    width : int
        Plot width in pixels.
    height : int
        Plot height in pixels.
    color_by_density : bool
        Color points by density instead of category.
    marker_line_width : float
        Width of marker border lines.
    marker_line_color : str
        Color of marker border lines.
    """

    # General Configuration
    # Allow extra parameters to pass through to Plotly
    model_config = ConfigDict(extra="allow")

    # Data mapping
    x: str = Field(..., description="Column for x-axis values.")
    y: str = Field(..., description="Column for y-axis values.")
    color: Optional[str] = Field(
        None, description="Column for color assignment (replaces 'group')."
    )
    symbol: Optional[str] = Field(
        None, description="Column for marker symbol assignment."
    )
    size: Optional[str] = Field(None, description="Column to determine marker size.")
    hover_name: Optional[str] = Field(
        None, description="Column for bold text in hover tooltip."
    )
    hover_data: List[str] = Field(
        [], description="Additional columns for hover tooltip."
    )
    text: Optional[str] = Field(None, description="Column for text labels on markers.")
    facet_row: Optional[str] = Field(None, description="Column for vertical facetting.")
    facet_col: Optional[str] = Field(
        None, description="Column for horizontal facetting."
    )
    error_x: Optional[str] = Field(None, description="Column for x-axis error bars.")
    error_y: Optional[str] = Field(None, description="Column for y-axis error bars.")
    labels: Optional[Dict[str, str]] = Field(
        None, description="Column name overrides for display purposes."
    )
    color_discrete_map: Optional[Dict[str, str]] = Field(
        None, description="Specific color mappings for color column values."
    )
    symbol_map: Optional[Dict[str, str]] = Field(
        None, description="Specific symbol mappings for symbol column values."
    )

    # Styling and Layout
    opacity: float = Field(0.8, ge=0, le=1, description="Overall opacity of markers.")
    size_max: int = Field(20, description="Maximum size for markers.")
    trendline: Optional[str] = Field(
        None, description="Trendline type (ols/lowess/rolling/expanding/ewm)."
    )
    trendline_options: Optional[Dict] = Field(
        None, description="Advanced options for trendline configuration."
    )
    log_x: bool = Field(False, description="Enable logarithmic x-axis scale.")
    log_y: bool = Field(False, description="Enable logarithmic y-axis scale.")
    range_x: Optional[List[float]] = Field(
        None, description="Manual x-axis range [min, max]."
    )
    range_y: Optional[List[float]] = Field(
        None, description="Manual y-axis range [min, max]."
    )
    title: str = Field("Scatter Plot", description="Main title of the plot.")
    subtitle: Optional[str] = Field(
        None, description="Subtitle displayed below main title."
    )
    template: str = Field("plotly_white", description="Plotly visual theme/template.")
    width: int = Field(800, description="Plot width in pixels.")
    height: int = Field(600, description="Plot height in pixels.")
    marker_line_width: float = Field(
        0.5, ge=0, description="Width of marker border lines."
    )
    marker_line_color: str = Field(
        "DarkSlateGrey", description="Color of marker border lines."
    )

    # Special features
    color_by_density: bool = Field(
        False, description="Color points by density instead of category."
    )

    @model_validator(mode="after")
    def validate_exclusive_color_options(self) -> "ScatterConfig":
        if self.color_by_density and self.color:
            raise ValueError(
                "Cannot use both 'color' and 'color_by_density'. "
                "These options are mutually exclusive."
            )
        return self
