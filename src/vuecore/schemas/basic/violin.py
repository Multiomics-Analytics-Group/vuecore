from typing import Optional
from pydantic import Field, ConfigDict
from vuecore.schemas.plotly_base import PlotlyBaseConfig


class ViolinConfig(PlotlyBaseConfig):
    """
    Pydantic model for validating and managing violin plot configurations,
    which extends PlotlyBaseConfig.

    This model serves as a curated API for the most relevant parameters
    for violin plots, closely aligned with the `plotly.express.violin` API
    (https://plotly.com/python-api-reference/generated/plotly.express.violin.html).

    It includes key parameters for data mapping, styling, and layout. It ensures
    that user-provided configurations are type-safe and adhere to the expected
    structure. The plotting function handles parameters defined here, and also
    accepts additional Plotly keyword arguments, forwarding them to the
    appropriate `plotly.express.violin` or `plotly.graph_objects.Figure` call.
    """

    # General Configuration
    # Allow extra parameters to pass through to Plotly
    model_config = ConfigDict(extra="allow")

    # Styling and Layout
    orientation: Optional[str] = Field(
        None,
        description="Orientation of the violin plots ('v' for vertical, 'h' for horizontal).",
    )
    violinmode: str = Field(
        "group", description="Mode for grouping violins ('group' or 'overlay')."
    )
    points: str | bool = Field(
        "outliers",
        description="Method to display sample points ('outliers', 'all', 'suspectedoutliers', False).",
    )
    box: bool = Field(False, description="If True, boxes are drawn inside the violins.")
