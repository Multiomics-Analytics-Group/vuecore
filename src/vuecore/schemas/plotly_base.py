from typing import Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict, model_validator


class PlotlyBaseConfig(BaseModel):
    """
    Pydantic model for common Plotly configurations.

    This model serves as a curated API for common parameters of Plotly plots,
    closely aligned with the `plotly.express` API
    (https://plotly.com/python-api-reference/plotly.express.html).

    This base class includes parameters shared across multiple plot types
    to ensure consistency and reduce code repetition. It uses a validator to
    enforce that at least one of the x or y axes is provided. Plot-specific
    schemas should inherit from this model.
    """

    model_config = ConfigDict(extra="allow")

    # Data Mapping
    x: Optional[str] = Field(None, description="Column for x-axis values.")
    y: Optional[str] = Field(None, description="Column for y-axis values.")
    color: Optional[str] = Field(
        None, description="Column to assign color to plot elements."
    )
    hover_name: Optional[str] = Field(
        None, description="Column to appear in bold in the hover tooltip."
    )
    hover_data: List[str] = Field(
        [], description="Additional columns for the hover tooltip."
    )
    facet_row: Optional[str] = Field(
        None, description="Column to create vertical subplots (facets)."
    )
    facet_col: Optional[str] = Field(
        None, description="Column to create horizontal subplots (facets)."
    )
    labels: Optional[Dict[str, str]] = Field(
        None,
        description="Dictionary to override column names for titles, legends, etc.",
    )
    color_discrete_map: Optional[Dict[str, str]] = Field(
        None, description="Specific color mappings for values in the `color` column."
    )
    category_orders: Optional[Dict[str, List[str]]] = Field(
        None, description="Dictionary to specify the order of categorical values."
    )

    # Styling and Layout
    log_x: bool = Field(False, description="If True, use a logarithmic x-axis.")
    log_y: bool = Field(False, description="If True, use a logarithmic y-axis.")
    range_x: Optional[List[float]] = Field(
        None, description="Range for the x-axis, e.g., [0, 100]."
    )
    range_y: Optional[List[float]] = Field(
        None, description="Range for the y-axis, e.g., [0, 100]."
    )
    title: str = Field("Plotly Plot", description="The main title of the plot.")
    x_title: Optional[str] = Field(None, description="Custom title for the x-axis.")
    y_title: Optional[str] = Field(None, description="Custom title for the y-axis.")
    subtitle: Optional[str] = Field(None, description="The subtitle of the plot.")
    template: str = Field("plotly_white", description="Plotly template for styling.")
    width: Optional[int] = Field(800, description="Width of the plot in pixels.")
    height: Optional[int] = Field(600, description="Height of the plot in pixels.")

    @model_validator(mode="after")
    def validate_x_or_y_provided(self) -> "PlotlyBaseConfig":
        """Ensure at least one of x or y is provided for the plot."""
        if self.x is None and self.y is None:
            raise ValueError(
                "At least one of 'x' or 'y' must be provided for the plot."
            )
        return self
