from vuecore import PlotType
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, model_validator


class ScatterConfig(BaseModel):
    """
    Pydantic model for validating and managing scatter plot configurations.

    This model defines all the possible parameters that can be used to customize
    a scatter plot, from data mapping to styling and layout. It ensures that
    user-provided configurations are type-safe and adhere to the expected structure.

    Attributes
    ---------
    x : str
        Column name for the x-axis.
    y : str
        Column name for the y-axis.
    type : Optional[PlotType]
        The type of plot. Defaults to `SCATTER`.
    group : Optional[str]
        Column for grouping data, typically used for coloring markers.
    size : Optional[str]
        Column to determine marker size, enabling a third dimension of data.
    symbol : Optional[str]
        Column to determine the shape of markers.
    text : Optional[str]
        Column for adding text labels directly onto markers.
    hover_cols : List[str]
        Additional data columns to display in the hover tooltip.
    title : str
        The main title of the plot.
    x_title : Optional[str]
        Custom title for the x-axis. If None, defaults to the `x` column name.
    y_title : Optional[str]
        Custom title for the y-axis. If None, defaults to the `y` column name.
    height : int
        Height of the plot in pixels.
    width : int
        Width of the plot in pixels.
    colors : Optional[Dict[str, str]]
        A dictionary mapping group names from the `group` column to specific colors.
    trendline : Optional[str]
        If specified, adds a trendline to the plot (e.g., 'ols', 'lowess').
    """

    # Data mapping
    x: str = Field(..., description="Column name for the x-axis.")
    y: str = Field(..., description="Column name for the y-axis.")
    type: Optional[PlotType] = Field(
        PlotType.SCATTER, description="Type of plot, defaults to SCATTER."
    )
    group: Optional[str] = Field(
        None, description="Column for grouping data, often used for color."
    )
    size: Optional[str] = Field(None, description="Column to determine marker size.")
    symbol: Optional[str] = Field(
        None, description="Column to determine marker symbol."
    )
    text: Optional[str] = Field(None, description="Column for text labels on markers.")
    hover_cols: List[str] = Field(
        [], description="Additional columns to show on hover."
    )

    # Styling and Layout
    title: str = Field("Scatter Plot", description="The main title of the plot.")
    x_title: Optional[str] = Field(
        None, description="Title for the x-axis. Defaults to x column name."
    )
    y_title: Optional[str] = Field(
        None, description="Title for the y-axis. Defaults to y column name."
    )
    height: int = Field(600, description="Height of the plot in pixels.")
    width: int = Field(800, description="Width of the plot in pixels.")
    colors: Optional[Dict[str, str]] = Field(
        None, description="Mapping of group names to specific colors."
    )
    marker_opacity: float = Field(
        0.8, ge=0, le=1, description="Opacity of the markers."
    )
    marker_line_width: float = Field(
        0.5, ge=0, description="Width of the line surrounding each marker."
    )
    marker_line_color: str = Field(
        "DarkSlateGrey", description="Color of the line surrounding each marker."
    )

    # Special features
    trendline: Optional[str] = Field(
        None, description="Adds a trendline. E.g., 'ols' for Ordinary Least Squares."
    )
    color_by_density: bool = Field(
        False, description="If True, color points by density instead of group."
    )

    @model_validator(mode="after")
    def check_exclusive_coloring(self) -> "ScatterConfig":
        """Ensure that coloring by group and by density are mutually exclusive."""
        if self.color_by_density and self.group:
            raise ValueError(
                "Cannot set 'group' when 'color_by_density' is True. "
                "Coloring is mutually exclusive."
            )
        return self
