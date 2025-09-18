# vuecore/schemas/basic/histogram.py

from typing import Dict, Optional
from pydantic import Field, ConfigDict
from vuecore.schemas.plotly_base import PlotlyBaseConfig


class HistogramConfig(PlotlyBaseConfig):
    """
    Pydantic model for validating and managing histogram plot configurations,
    which extends PlotlyBaseConfig.

    This model serves as a curated API for the most relevant parameters
    for histogram plots, closely aligned with the `plotly.express.histogram` API
    (https://plotly.com/python-api-reference/generated/plotly.express.histogram.html).

    This model includes the most relevant parameters for data mapping, styling,
    and layout. It ensures that user-provided configurations are type-safe and
    adhere to the expected structure. The plotting function handles parameters
    defined here, and also accepts additional Plotly keyword arguments,
    forwarding them to the appropriate `plotly.express.histogram` or
    `plotly.graph_objects.Figure` call.
    """

    # General Configuration
    # Allow extra parameters to pass through to Plotly
    model_config = ConfigDict(extra="allow")

    # Data Mapping
    pattern_shape: Optional[str] = Field(
        None, description="Column to assign pattern shapes to bars."
    )
    pattern_shape_map: Optional[Dict[str, str]] = Field(
        None, description="Map values to specific pattern shapes."
    )

    # Styling and Layout
    marginal: Optional[str] = Field(
        None,
        description="Adds a marginal subplot ('rug', 'box', 'violin', 'histogram').",
    )
    opacity: float = Field(0.8, description="Overall opacity of the bars.")
    orientation: Optional[str] = Field(
        None,
        description="Orientation of the bars ('v' for vertical, 'h' for horizontal).",
    )
    barmode: str = Field("relative", description="Mode for grouping bars.")
    barnorm: Optional[str] = Field(
        None, description="Normalization mode for stacked bars ('fraction', 'percent')."
    )
    histnorm: Optional[str] = Field(
        None,
        description="Normalization mode for the histogram ('percent', 'probability', 'density', 'probability density').",
    )
    histfunc: Optional[str] = Field(
        "count",
        description="Function used to aggregate values ('count', 'sum', 'avg', 'min', 'max').",
    )
    cumulative: bool = Field(
        False, description="If True, histogram values are cumulative."
    )
    nbins: Optional[int] = Field(None, description="Sets the number of bins.")
    text_auto: bool = Field(False, description="If True, displays text labels on bars.")
