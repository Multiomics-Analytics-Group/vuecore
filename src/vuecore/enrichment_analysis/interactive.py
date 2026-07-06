# %%
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

DIRECTION_COLORS = {
    "upregulated": "#cb181d",
    "downregulated": "#3288bd",
    "regulated": "#ae017e",
    "non-regulated": "#fcc5c0",
}

ENRICHMENT_HOVERING_COLS = [
    "foreground",
    "foreground_pop",
    "background",
    "background_pop",
    "pvalue",
    "padj",
    "identifiers",
]


def get_scatterplot(
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

        result = get_scatterplot(
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


def get_enrichment_plots(
    enrichment_results,
    width=900,
    height=800,
    title="Enrichment",
    colors=DIRECTION_COLORS,
    hovering_cols=ENRICHMENT_HOVERING_COLS,
):
    """
    This function generates a scatter plot with enriched terms (y-axis)
    and their adjusted pvalues (x-axis)

    :param pandas.DataFrame enrichment_results: dataframe with the enrichment data to plot
                                         (see enrichment functions for format)
    :param int width: plot width.
    :param int height: plot height.
    :param str title: title of the figure.
    :param dict colors: dictionary with colors to be used for each direction/group.
    :param list hovering_cols: list of columns in dataframe that will be shown when
                                hovering over a dot.
    :return list: list of scatter plots one for each enrichment table available
                  (i.e pairwise comparisons)

    Example::

        figure = get_enrichment_plots(df, width=1500, height=800, title="Enrichment")
    """
    figures = []

    if not isinstance(enrichment_results, dict):
        enrichment_results = {"regulated~non-regulated": enrichment_results.copy()}

    for g, table in enrichment_results.items():
        if table.empty:
            continue
        df = table[table.rejected]
        if df.empty:
            continue
        group = "direction" if "direction" in df else None
        df = df.sort_values(by=[group, "padj"], ascending=False)
        df["x"] = -np.log10(df["padj"])

        g1, g2 = g.split("~")
        fig = get_scatterplot(
            df,
            x="x",
            y="terms",
            group=group,
            symbol=group,
            size="foreground",
            hovering_cols=hovering_cols,
            title="{} {} vs {}".format(title, g1, g2),
            x_title="-log10(padj)",
            y_title="Enriched terms",
            width=width,
            height=height,
            colors=colors,
        )
        figures.append(fig)

    return figures


# %%
if __name__ == "__main__":
    # %%
    import pandas as pd

    fname = "/Users/heweb/Documents/repos/vuecore/tests/data/enrichment_analysis.csv"
    enrichment_results = pd.read_csv(fname, index_col=0)

    # %%
    figures = get_enrichment_plots(enrichment_results, width=1500, height=800, title="Enrichment")
    figures[0]
