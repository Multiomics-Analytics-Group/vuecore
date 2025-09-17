from enum import auto

try:
    from enum import StrEnum
except ImportError:
    # Fallback for Python versions < 3.11 that don't have StrEnum built-in
    from strenum import StrEnum


class PlotType(StrEnum):
    """Enum representing supported plot types."""

    SCATTER = auto()
    LINE = auto()
    BAR = auto()
    BOX = auto()
    VIOLIN = auto()
    HISTOGRAM = auto()


class EngineType(StrEnum):
    """Enum representing supported plotting engines."""

    PLOTLY = auto()
    # Add other engines as needed


class OutputFileFormat(StrEnum):
    """Enum representing supported output file formats."""

    PNG = auto()
    JPG = auto()
    JPEG = auto()
    SVG = auto()
    PDF = auto()
    HTML = auto()
    JSON = auto()
    WEBP = auto()

    @property
    def value_with_dot(self):
        """Return the file extension with the dot (e.g., '.png')."""
        return f".{self.value}"
