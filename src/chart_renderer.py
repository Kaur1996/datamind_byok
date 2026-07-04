import json
import pandas as pd
import plotly.express as px

def chart_render(chart_jsn, path):
    chart_jsn = json.loads(chart_jsn)
    input_df = pd.read_csv(path, header=0, encoding='latin1')
    
    #loop_len = chart_jsn.len()
    charts_list = chart_jsn["charts"]
    all_figs = []

    for x in charts_list:
        title = x["title"]
        x_axis = x["x_axis"]
        y_axis = x["y_axis"]
        chart_type = x["chart_type"]
        col = x.get("colour")

        try:
            if chart_type == "histogram":
                fig = px.histogram(input_df, x=x_axis, color=col, title=title)
            else:
                plot_func = getattr(px, chart_type)
                fig = plot_func(input_df, x=x_axis, y=y_axis, color=col, title=title)

            all_figs.append(fig)

        except Exception as e:
            print(f"Skipping chart '{title}' — unsupported chart_type '{chart_type}': {e}")
        continue

    return all_figs

if __name__ == "__main__":
    with open("data/cached_charts.json", "r") as f:
        chart_jsn = f.read()

    figs = chart_render(chart_jsn, "data/Superstore.csv")

    print(f"Returned {len(figs)} figures")
    for fig in figs:
        fig.show()   # opens each chart in your default browser
