from enum import auto

try:
    from enum import StrEnum
except ImportError:
    from strenum import StrEnum


class PlotType(StrEnum):
    SCATTER = auto()
    LINE = auto()
    BAR = auto()


class EngineType(StrEnum):
    PLOTLY = auto()
    # Add other engines as needed
