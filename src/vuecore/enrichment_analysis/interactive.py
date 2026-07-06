# %%
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


def get_scatterplot(data, args):
    """
    This function plots a simple Scatterplot.

    :param data: is a Pandas DataFrame with four columns: "name", x values and y values
                 (provided as variables) to plot.
    :param dict args: see below.
    :Arguments:
        * **title** (str) -- title of the figure.
        * **x** (str) -- column in dataframe with values for x
        * **y** (str) -- column in dataframe with values for y
        * **group** (str) -- column in dataframe with the groups - translates into colors \
                             (default None)
        * **hovering_cols** (list) -- list of columns in dataframe that will be shown when \
                                      hovering over a dot
        * **size**  (str) -- column in dataframe that contains the size of the dots (default None)
        * **trendline** (bool) -- whether or not to draw a trendline
        * **text** (str) -- column in dataframe that contains the values shown for each dot
        * **x_title** (str) -- plot x axis title.
        * **y_title** (str) -- plot y axis title.
        * **height** (int) -- plot height.
        * **width** (int) -- plot width.
        * **colors** (dict) -- dictionary with colors to be used for each group
    :return: scatterplot figure within the <div id="_dash-app-content">.

    Example::

        result = get_scatterplot(data,
                                 identifier='scatter plot',
                                 args={'title':'Scatter Plot',
                                        'x_title':'x_axis',
                                        'y_title':'y_axis',
                                        'height':100,
                                        'width':100}
                                )
    """
    annotation = []
    title = "Scatter plot"
    x_title = "x"
    y_title = "y"
    height = 800
    width = 800
    size = None
    symbol = None
    x = "x"
    y = "y"
    trendline = None
    group = None
    text = None
    if "x" in args:
        x = args["x"]
    if "y" in args:
        y = args["y"]
    if "group" in args:
        group = args["group"]
    if "hovering_cols" in args:
        annotation = args["hovering_cols"]
    if "title" in args:
        title = args["title"]
    if "x_title" in args:
        x_title = args["x_title"]
    if "y_title" in args:
        y_title = args["y_title"]
    if "height" in args:
        height = args["height"]
    if "width" in args:
        width = args["width"]
    if "size" in args:
        size = args["size"]
    if "symbol" in args:
        symbol = args["symbol"]
    if "trendline" in args:
        trendline = args["trendline"]
    if "text" in args:
        text = args["text"]

    colors = None
    if "colors" in args and isinstance(args["colors"], dict):
        colors = args["colors"]

    figure = px.scatter(
        data,
        x=x,
        y=y,
        color=group,
        color_discrete_map=colors,
        hover_data=annotation,
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


# ! define schema for enrichment_results
def get_enrichment_plots(enrichment_results, args):
    """
    This function generates a scatter plot with enriched terms (y-axis)
    and their adjusted pvalues (x-axis)

    :param pandas.DataFrame enrichment_results: dataframe with the enrichment data to plot
                                         (see enrichment functions for format)
    :param dict args: dictionary containing the arguments needed to plot the figure
                      (width, height, title)
    :return list: list of scatter plots one for each enrichment table available
                  (i.e pairwise comparisons)

    Example::

        figure = get_enrichment_plots(df,
                                     identifier='enrichment',
                                     args={'width':1500,
                                           'height':800,
                                           'title':'Enrichment'}
                                    )
    """
    figures = []
    width = 900
    height = 800
    colors = {
        "upregulated": "#cb181d",
        "downregulated": "#3288bd",
        "regulated": "#ae017e",
        "non-regulated": "#fcc5c0",
    }
    title = "Enrichment"
    if "width" in args:
        width = args["width"]
    if "height" in args:
        height = args["height"]
    if "title" in args:
        title = args["title"]

    if not isinstance(enrichment_results, dict):
        aux = enrichment_results.copy()
        enrichment_results = {"regulated~non-regulated": aux}

    for g in enrichment_results:
        g1, g2 = g.split("~")
        group = "direction"
        if not enrichment_results[g].empty:
            df = enrichment_results[g][enrichment_results[g].rejected]
            if "direction" not in df:
                group = None
            if not df.empty:
                df = df.sort_values(by=[group, "padj"], ascending=False)
                df["x"] = -np.log10(df["padj"])
                fig = get_scatterplot(
                    df,
                    args={
                        "x": "x",
                        "y": "terms",
                        "group": group,
                        "title": "{} {} vs {}".format(title, g1, g2),
                        "symbol": group,
                        "colors": colors,
                        "x_title": "-log10(padj)",
                        "y_title": "Enriched terms",
                        "width": width,
                        "height": height,
                        "hovering_cols": [
                            "foreground",
                            "foreground_pop",
                            "background",
                            "background_pop",
                            "pvalue",
                            "padj",
                            "identifiers",
                        ],
                        "size": "foreground",
                    },
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
    figures = get_enrichment_plots(
        enrichment_results, args={"width": 1500, "height": 800, "title": "Enrichment"}
    )
    figures[0]
