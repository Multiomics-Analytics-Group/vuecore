from typing import Dict, Optional
from pydantic import Field, ConfigDict
from vuecore.schemas.plotly_base import PlotlyBaseConfig


class BarConfig(PlotlyBaseConfig):
    """
    Pydantic model for validating and managing bar plot configurations,
    which extends PlotlyBaseConfig.

    This model serves as a curated API for the most relevant parameters
    for bar plots, closely aligned with the `plotly.express.bar` API
    (https://plotly.com/python-api-reference/generated/plotly.express.bar.html).

    This model includes the most relevant parameters for data mapping, styling,
    and layout. It ensures that user-provided configurations are type-safe and
    adhere to the expected structure. The plotting function handles parameters
    defined here, and also accepts additional Plotly keyword arguments,
    forwarding them to the appropriate `plotly.express.bar` or
    `plotly.graph_objects.Figure` call.
    """

    # General Configuration
    # Allow extra parameters to pass through to Plotly
    model_config = ConfigDict(extra="allow")

    # Data Mapping
    pattern_shape: Optional[str] = Field(
        None, description="Column to assign pattern shapes to bars."
    )
    text: Optional[str] = Field(None, description="Column for text labels on bars.")
    error_x: Optional[str] = Field(None, description="Column for x-axis error bars.")
    error_y: Optional[str] = Field(None, description="Column for y-axis error bars.")
    pattern_shape_map: Optional[Dict[str, str]] = Field(
        None, description="Map values to specific pattern shapes."
    )

    # Styling and Layout
    opacity: float = Field(0.8, description="Overall opacity of markers.")
    orientation: str = Field(
        "v",
        description="Orientation of the bars ('v' for vertical, 'h' for horizontal).",
    )
    barmode: str = Field("relative", description="Mode for grouping bars.")
