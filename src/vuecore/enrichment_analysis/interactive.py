# %%
from logging import getLogger
from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from acore.types.enrichment_analysis import EnrichmentAnalysisSchema
from pandera.typing.pandas import DataFrame

from vuecore.enrichment_analysis.common import (
    build_color_map,
    format_comparison_title,
)

logger = getLogger(__name__)

ENRICHMENT_HOVERING_COLS = [
    "foreground",
    "foreground_pop",
    "background",
    "background_pop",
    "pvalue",
    "padj",
    "identifiers",
]


def get_enrichment_plot_plotly(
    data,
    x="x",
    y="y",
    group=None,
    hovering_cols=None,
    size=None,
    symbol=None,
    trendline=None,
    text=None,
    title="Scatter plot",
    x_title="x",
    y_title="y",
    height=800,
    width=800,
    colors=None,
):
    """
    This function plots a simple Scatterplot.

    :param data: is a Pandas DataFrame with four columns: "name", x values and y values
                 (provided as variables) to plot.
    :param str x: column in dataframe with values for x
    :param str y: column in dataframe with values for y
    :param str group: column in dataframe with the groups - translates into colors
    :param list hovering_cols: list of columns in dataframe that will be shown when
                                hovering over a dot
    :param str size: column in dataframe that contains the size of the dots
    :param str symbol: column in dataframe that contains the symbol of the dots
    :param bool trendline: whether or not to draw a trendline
    :param str text: column in dataframe that contains the values shown for each dot
    :param str title: title of the figure.
    :param str x_title: plot x axis title.
    :param str y_title: plot y axis title.
    :param int height: plot height.
    :param int width: plot width.
    :param dict colors: dictionary with colors to be used for each group
    :return: scatterplot figure within the <div id="_dash-app-content">.

    Example::

        result = get_enrichment_plot_plotly(
            data,
            title="Scatter Plot",
            x_title="x_axis",
            y_title="y_axis",
            height=100,
            width=100,
        )
    """
    figure = px.scatter(
        data,
        x=x,
        y=y,
        color=group,
        color_discrete_map=colors,
        hover_data=hovering_cols,
        size=size,
        symbol=symbol,
        trendline=trendline,
        text=text,
    )

    figure.update_traces(
        marker=dict(size=14, opacity=0.7, line=dict(width=0.5, color="DarkSlateGrey")),
        selector=dict(mode="markers"),
    )
    figure["layout"] = go.Layout(
        title=title,
        xaxis={"title": x_title},
        yaxis={"title": y_title},
        legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="right", x=1),
        hovermode="closest",
        height=height,
        width=width,
        annotations=[dict(xref="paper", yref="paper", showarrow=False, text="")],
        template="plotly_white",
    )

    return figure


# acore related plotting function using a defined type in acore.types
# ToDo: move to acore.plotting?
def get_enrichment_plot(
    enrichment_results: Union[pd.DataFrame, DataFrame[EnrichmentAnalysisSchema]],
    comparison: Optional[str] = None,
    width: int = 900,
    height: int = 800,
    title: str = "Enrichment",
    colors: Optional[Union[Dict[str, str], List[str]]] = None,
    hovering_cols: list = ENRICHMENT_HOVERING_COLS,
    **kwargs,
) -> go.Figure:
    """
    Create an interactive enrichment scatter plot for a single comparison.

    Parameters
    ----------
    enrichment_results : Union[pd.DataFrame, DataFrame[EnrichmentAnalysisSchema]]
        Enrichment results validated against `EnrichmentAnalysisSchema`, with
        one or more comparisons stacked in the 'comparison' column.
    comparison : str, optional
        Comparison to plot. Required when more than one comparison is present;
        inferred automatically when there is only one.
    width : int, optional
        Plot width.
    height : int, optional
        Plot height.
    title : str, optional
        Base title for the plot.
    colors : dict[str, str] or list[str], optional
        Color mapping by direction, or a palette to assign to directions in
        order. Defaults to a built-in palette, cycling if there are more
        unique directions than colors.
    hovering_cols : list, optional
        Hover columns shown in tooltips.
    **kwargs : dict
        Additional keyword arguments for API parity with the static version.

    Returns
    -------
    plotly.graph_objects.Figure
        The scatter plot for the selected comparison.
    """
    df: pd.DataFrame = EnrichmentAnalysisSchema.validate(enrichment_results)

    if kwargs:
        logger.info(f"Additional unused kwargs passed to get_enrichment_plot: {kwargs}")

    available = sorted(df["comparison"].unique())
    if comparison is None:
        if len(available) > 1:
            raise ValueError(
                "Multiple comparisons are available: "
                f"{', '.join(available)}. Pass `comparison` to select one."
            )
        comparison = available[0]
    elif comparison not in available:
        raise ValueError(
            f"Comparison '{comparison}' not found. Available comparisons: "
            f"{', '.join(available)}."
        )

    df = df.query("comparison == @comparison and rejected").copy()
    df = df.sort_values(by=["direction", "padj"], ascending=False).reset_index(
        drop=True
    )
    df["x"] = -np.log10(df["padj"])
    colors = build_color_map(df["direction"], colors)

    return get_enrichment_plot_plotly(
        df,
        x="x",
        y="terms",
        group="direction",
        symbol="direction",
        size="foreground",  # column foreground in enrichment_result
        hovering_cols=hovering_cols,
        title=format_comparison_title(title, comparison),
        x_title="-log10(padj)",
        y_title="Enriched terms",
        width=width,
        height=height,
        colors=colors,
    )


# %%
if __name__ == "__main__":
    # %%
    import pandas as pd

    fname = "/Users/heweb/Documents/repos/vuecore/tests/data/enrichment_analysis.csv"
    enrichment_results = pd.read_csv(fname, index_col=0)

    figure = get_enrichment_plot(
        enrichment_results, width=1500, height=800, title="Enrichment"
    )
    figure.show()

# %%
