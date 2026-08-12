from __future__ import annotations

from pydantic import ConfigDict, Field

from vuecore.schemas.plotly_base import PlotlyBaseConfig


class LineConfig(PlotlyBaseConfig):
    """
    Pydantic model for validating and managing line plot configurations,
    which extends PlotlyBaseConfig.

    This model serves as a curated API for the most relevant parameters
    for line plots, closely aligned with the `plotly.express.line` API
    (https://plotly.com/python-api-reference/generated/plotly.express.line.html).

    This model includes the most relevant parameters for data mapping, styling,
    and layout. It ensures that user-provided configurations are type-safe and
    adhere to the expected structure. The plotting function handles parameters
    defined here, and also accepts additional Plotly keyword arguments,
    forwarding them to the appropriate `plotly.express.line` or
    `plotly.graph_objects.Figure` call.
    """

    # General Configuration
    # Allow extra parameters to pass through to Plotly
    model_config = ConfigDict(extra="allow")

    # Data Mapping
    line_group: str | None = Field(
        None, description="Column to group data into separate lines."
    )
    line_dash: str | None = Field(
        None, description="Column to assign dash styles to lines."
    )
    symbol: str | None = Field(None, description="Column to assign symbols to markers.")
    text: str | None = Field(None, description="Column for text labels on markers.")
    error_x: str | None = Field(None, description="Column for x-axis error bars.")
    error_y: str | None = Field(None, description="Column for y-axis error bars.")
    line_dash_map: dict[str, str] | None = Field(
        None, description="Map values to specific dash styles."
    )
    symbol_map: dict[str, str] | None = Field(
        None, description="Map values to specific symbols."
    )

    # Styling and Layout
    markers: bool = Field(False, description="If True, displays markers on the lines.")
    line_shape: str | None = Field(
        "linear", description="Line shape (e.g., 'linear', 'spline')."
    )
