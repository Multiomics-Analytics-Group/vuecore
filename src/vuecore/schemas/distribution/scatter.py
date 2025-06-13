from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ScatterConfig(BaseModel):
    """
    Pydantic model for validating and managing scatter plot configurations.

    This model defines all the possible parameters that can be used to customize
    a scatter plot, from data mapping to styling and layout. It ensures that
    user-provided configurations are type-safe and adhere to the expected structure.

    Attributes
    ----------
    x : str
        Column name for the x-axis.
    y : str
        Column name for the y-axis.
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

    # Special features
    trendline: Optional[str] = Field(
        None, description="Adds a trendline. E.g., 'ols' for Ordinary Least Squares."
    )
