from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator


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
    x: str | None = Field(None, description="Column for x-axis values.")
    y: str | None = Field(None, description="Column for y-axis values.")
    color: str | None = Field(
        None, description="Column to assign color to plot elements."
    )
    hover_name: str | None = Field(
        None, description="Column to appear in bold in the hover tooltip."
    )
    hover_data: list[str] = Field(
        [], description="Additional columns for the hover tooltip."
    )
    facet_row: str | None = Field(
        None, description="Column to create vertical subplots (facets)."
    )
    facet_col: str | None = Field(
        None, description="Column to create horizontal subplots (facets)."
    )
    labels: dict[str, str] | None = Field(
        None,
        description="Dictionary to override column names for titles, legends, etc.",
    )
    color_discrete_map: dict[str, str] | None = Field(
        None, description="Specific color mappings for values in the `color` column."
    )
    category_orders: dict[str, list[str]] | None = Field(
        None, description="Dictionary to specify the order of categorical values."
    )

    # Styling and Layout
    log_x: bool = Field(False, description="If True, use a logarithmic x-axis.")
    log_y: bool = Field(False, description="If True, use a logarithmic y-axis.")
    range_x: list[float] | None = Field(
        None, description="Range for the x-axis, e.g., [0, 100]."
    )
    range_y: list[float] | None = Field(
        None, description="Range for the y-axis, e.g., [0, 100]."
    )
    title: str = Field("Plotly Plot", description="The main title of the plot.")
    x_title: str | None = Field(None, description="Custom title for the x-axis.")
    y_title: str | None = Field(None, description="Custom title for the y-axis.")
    subtitle: str | None = Field(None, description="The subtitle of the plot.")
    template: str = Field("plotly_white", description="Plotly template for styling.")
    width: int | None = Field(800, description="Width of the plot in pixels.")
    height: int | None = Field(600, description="Height of the plot in pixels.")

    @model_validator(mode="after")
    def validate_x_or_y_provided(self) -> PlotlyBaseConfig:
        """Ensure at least one of x or y is provided for the plot."""
        if self.x is None and self.y is None:
            raise ValueError(
                "At least one of 'x' or 'y' must be provided for the plot."
            )
        return self
