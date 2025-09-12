from typing import Optional
from pydantic import Field, ConfigDict
from vuecore.schemas.plotly_base import PlotlyBaseConfig


class BoxConfig(PlotlyBaseConfig):
    """
    Pydantic model for validating and managing box plot configurations,
    which extends PlotlyBaseConfig.

    This model serves as a curated API for the most relevant parameters
    for box plots, closely aligned with the `plotly.express.box` API
    (https://plotly.com/python-api-reference/generated/plotly.express.box.html).

    It includes key parameters for data mapping, styling, and layout. It ensures
    that user-provided configurations are type-safe and adhere to the expected
    structure. The plotting function handles parameters defined here, and also
    accepts additional Plotly keyword arguments, forwarding them to the
    appropriate `plotly.express.box` or `plotly.graph_objects.Figure` call.
    """

    # General Configuration
    # Allow extra parameters to pass through to Plotly
    model_config = ConfigDict(extra="allow")

    # Styling and Layout
    orientation: Optional[str] = Field(
        None,
        description="Orientation of the box plots ('v' for vertical, 'h' for horizontal).",
    )
    boxmode: str = Field("group", description="Mode for grouping boxes.")
    notched: bool = Field(False, description="If True, boxes are drawn with notches.")
    points: str = Field(
        "outliers",
        description="Method to display sample points ('outliers', 'all', 'suspectedoutliers', False).",
    )
