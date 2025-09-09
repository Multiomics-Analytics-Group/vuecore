from typing import Dict, Optional
from pydantic import Field, ConfigDict, model_validator
from vuecore.schemas.plotly_base import PlotlyBaseConfig


class ScatterConfig(PlotlyBaseConfig):
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
    """

    # General Configuration
    # Allow extra parameters to pass through to Plotly
    model_config = ConfigDict(extra="allow")

    # Data Mapping
    symbol: Optional[str] = Field(None, description="Column to assign marker symbols.")
    size: Optional[str] = Field(None, description="Column to determine marker size.")
    text: Optional[str] = Field(None, description="Column for text labels on markers.")
    error_x: Optional[str] = Field(None, description="Column for x-axis error bars.")
    error_y: Optional[str] = Field(None, description="Column for y-axis error bars.")
    symbol_map: Optional[Dict[str, str]] = Field(
        None, description="Specific symbol mappings for symbol column values."
    )
    size_max: int = Field(20, description="Maximum size for markers.")

    # Styling and Layout
    opacity: float = Field(0.8, description="Overall opacity of markers.")
    trendline: Optional[str] = Field(
        None, description="Trendline type (ols/lowess/rolling/expanding/ewm)."
    )
    trendline_options: Optional[Dict] = Field(
        None, description="Advanced options for trendline configuration."
    )
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
                "Cannot use both 'color_by_density' and 'color' parameters. "
                "Please choose only one for coloring the markers."
            )
        return self
