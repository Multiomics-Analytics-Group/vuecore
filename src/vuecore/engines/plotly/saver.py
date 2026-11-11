from pathlib import Path

import kaleido
import plotly.graph_objects as go

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
    RuntimeError
        If the figure cannot be saved, for example because the file extension is
        not one of the supported formats, the destination folder does not exist or
        the destination is not writable. The error that caused it is named in the
        message and chained as ``__cause__``. No folder is created.
    """
    path = Path(filepath)
    suffix = path.suffix.lower()

    supported_suffixes = [f.value_with_dot for f in OutputFileFormat]

    try:
        # Plotly does not create the folder, and its own error for a missing one
        # names only the file. Not checked for an unsupported format, which is
        # rejected below, and which is then the error that is described.
        if suffix in supported_suffixes and not path.parent.is_dir():
            raise FileNotFoundError(
                f"The destination folder '{path.parent}' is not an existing folder."
            )

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
            listed_suffixes = ", ".join(f"'{s}'" for s in supported_suffixes)
            raise ValueError(
                f"Unsupported file format: '{suffix}'. "
                f"Supported formats: {listed_suffixes}"
            )
    except Exception as e:
        # Catch any exceptions during the saving process and re-raise as a RuntimeError.
        # The cause is in the message too, as a caller that prints only the message
        # would otherwise not see why the file could not be written.
        raise RuntimeError(
            f"[VueCore] Failed to save plot: {filepath}. {type(e).__name__}: {e}"
        ) from e

    print(f"[VueCore] Plot saved to {filepath}")
