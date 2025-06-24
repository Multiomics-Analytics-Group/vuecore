import plotly.graph_objects as go
import plotly.io as pio
import kaleido
from pathlib import Path


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

    Examples
    --------
    >>> import plotly.express as px
    >>> fig = px.scatter(x=[1, 2, 3], y=[1, 2, 3])
    >>> # Save as an interactive HTML file
    >>> save(fig, 'scatter.html')
    Plot saved to scatter.html
    >>> # Save as a static PNG image
    >>> save(fig, 'scatter.png')
    Plot saved to scatter.png
    """
    path = Path(filepath)
    suffix = path.suffix.lower()

    try:
        if suffix in [".png", ".jpg", ".jpeg", ".webp", ".svg", ".pdf"]:
            try:
                fig.write_image(filepath)
            except RuntimeError as e:
                if "Kaleido requires Google Chrome" in str(e):
                    print(
                        "[VueCore] Chrome not found. Attempting automatic install using `kaleido.get_chrome_sync()`..."
                    )
                    try:
                        kaleido.get_chrome_sync()
                        fig.write_image(filepath)  # Retry after installing Chrome
                    except Exception as install_error:
                        raise RuntimeError(
                            "[VueCore] Failed to install Chrome automatically. "
                            "Please install it manually or run `plotly_get_chrome`."
                        ) from install_error
                else:
                    raise
        elif suffix == ".html":
            fig.write_html(filepath, include_plotlyjs="cdn")
        else:
            raise ValueError(
                f"Unsupported file format: '{suffix}'. "
                "Supported formats: .png, .svg, .pdf, .html, .json"
            )
    except Exception as e:
        raise RuntimeError(f"[VueCore] Failed to save plot: {filepath}") from e

    print(f"[VueCore] Plot saved to {filepath}")
