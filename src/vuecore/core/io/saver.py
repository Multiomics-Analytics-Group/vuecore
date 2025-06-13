import plotly.graph_objects as go
from pathlib import Path


def save_plot(fig: go.Figure, filepath: str) -> None:
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
    >>> save_plot(fig, 'scatter.html')
    Plot saved to scatter.html
    >>> # Save as a static PNG image
    >>> save_plot(fig, 'scatter.png')
    Plot saved to scatter.png
    """
    path = Path(filepath)
    suffix = path.suffix.lower()

    if suffix in [".png", ".jpg", ".jpeg", ".webp", ".svg", ".pdf"]:
        fig.write_image(filepath)
    elif suffix == ".html":
        fig.write_html(filepath, include_plotlyjs="cdn")
    elif suffix == ".json":
        fig.write_json(filepath)
    else:
        raise ValueError(
            f"Unsupported file format: '{suffix}'. Supported formats: .png, .svg, .pdf, .html, .json"
        )

    print(f"Plot saved to {filepath}")
