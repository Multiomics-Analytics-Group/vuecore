from enum import auto

try:
    from enum import StrEnum
except ImportError:
    from strenum import StrEnum


class PlotType(StrEnum):
    SCATTER = auto()
    LINE = auto()
    # Add other plot types as needed


class EngineType(StrEnum):
    PLOTLY = auto()
    # Add other engines as needed
