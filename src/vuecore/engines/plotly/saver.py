import plotly.graph_objects as go
import kaleido
from pathlib import Path

from vuecore.constants import OutputFileFormat


def save(fig: go.Figure, filepath: str) -> None:
    """
    Saves a Plotly figure to a file, inferring the format from the extension.

    This utility provides a single interface for exporting a figure to various
    static and interactive formats.

    Parameters
    ----------
    fig : go.Figure
        The Plotly figure object to save.
    filepath : str
        The destination path for the file (e.g., 'my_plot.png', 'figure.html').
        The format is determined by the file extension.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the file extension is not one of the supported formats.
    ImportError
        If required libraries for image export (e.g., kaleido) are not installed.
    """
    path = Path(filepath)
    suffix = path.suffix.lower()

    try:
        # Define static suffixes from the OutputFileFormat enum
        image_suffixes = [
            OutputFileFormat.PNG.value_with_dot,
            OutputFileFormat.JPG.value_with_dot,
            OutputFileFormat.JPEG.value_with_dot,
            OutputFileFormat.WEBP.value_with_dot,
            OutputFileFormat.SVG.value_with_dot,
            OutputFileFormat.PDF.value_with_dot,
        ]

        if suffix in image_suffixes:
            try:
                fig.write_image(filepath)
            except RuntimeError as e:
                # Handle specific Kaleido errors for Chrome installation
                if "Kaleido requires Google Chrome" in str(e):
                    print(
                        "[VueCore] Chrome not found. Attempting automatic install using `kaleido.get_chrome_sync()`..."
                    )
                    try:
                        kaleido.get_chrome_sync()
                        # Retry after installing Chrome
                        fig.write_image(filepath)
                    except Exception as install_error:
                        raise RuntimeError(
                            "[VueCore] Failed to install Chrome automatically. "
                            "Please install it manually or run `plotly_get_chrome`."
                        ) from install_error
                else:
                    raise  # Re-raise other RuntimeError exceptions
        elif suffix == OutputFileFormat.HTML.value_with_dot:
            fig.write_html(filepath, include_plotlyjs="cdn")
        elif suffix == OutputFileFormat.JSON.value_with_dot:
            fig.write_json(
                filepath, pretty=True
            )  # Added pretty=True for readable JSON output
        else:
            # Generate a dynamic list of supported formats for the error message
            supported_suffixes = ", ".join(
                [f"'{f.value_with_dot}'" for f in OutputFileFormat]
            )
            raise ValueError(
                f"Unsupported file format: '{suffix}'. "
                f"Supported formats: {supported_suffixes}"
            )
    except Exception as e:
        # Catch any exceptions during the saving process and re-raise as a RuntimeError
        raise RuntimeError(f"[VueCore] Failed to save plot: {filepath}") from e

    print(f"[VueCore] Plot saved to {filepath}")
