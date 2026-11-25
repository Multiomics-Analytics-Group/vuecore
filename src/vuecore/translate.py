import base64
import io

import matplotlib.figure

from dash import html


def hex2rgb(color: str) -> tuple[int, int, int, float]:
    _hex = color.lstrip("#")
    rgb = tuple(int(_hex[i : i + 2], 16) for i in (0, 2, 4))
    rgba = rgb + (0.6,)
    return rgba


def mpl_to_html_image(plot: matplotlib.figure.Figure, width: int = 800) -> html.Img:
    buf = io.BytesIO()
    plot.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("utf8")
    figure = html.Img(src=f"data:image/png;base64,{data}", width=f"{width}")

    return figure
