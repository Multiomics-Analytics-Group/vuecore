from typing import Optional, Union
import pandas as pd
import numpy as np
from pydantic import Field, ConfigDict
from vuecore.schemas.plotly_base import PlotlyBaseConfig
from pydantic import BaseModel, Field, ConfigDict, model_validator

class ScatterMapConfig(BaseModel):
    """
    Pydantic model for validating and managing scatter map plot configurations,
    which extends PlotlyBaseConfig.

    This model serves as a curated API for the most relevant parameters
    for scatter map plots, closely aligned with the `plotly.express.scatter_map` API
    (https://plotly.com/python-api-reference/generated/plotly.express.scatter_map.html).

    It includes key parameters for data mapping, styling, and layout. It ensures
    that user-provided configurations are type-safe and adhere to the expected
    structure. The plotting function handles parameters defined here, and also
    accepts additional Plotly keyword arguments, forwarding them to the
    appropriate `plotly.express.scatter_map` or `plotly.graph_objects.Figure` call.
    """

    # General Configuration
    # Allow extra parameters to pass through to Plotly
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

    # Data Mapping
    lat: Optional[Union[str, int, pd.Series]] = Field(None, description="Column for latitude values.")
    lon: Optional[Union[str, int, pd.Series]] = Field(None, description="Column for longitude values.")
    size: Optional[Union[str, int, pd.Series, list, np.ndarray]] = Field(None, description="Column to determine marker sizes. Or int or series.")
    size_max: int = Field(20, description="Maximum size of the markers.")

    zoom: int = Field(1, description="Initial zoom level of the map.")
    center: Optional[dict] = Field(
        None,
        description="Initial center of the map as a dict with 'lat' and 'lon'.",
    )

    title: str = Field("Scatter Geo Plot", description="The main title of the plot.")
    color_continuous_scale: Optional[str] = Field(
        None,
        description="Color scale for continuous color mapping (e.g., 'Viridis', 'Cividis').",
    )