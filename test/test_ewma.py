import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
import sys
sys.path.append("/home/nick/Control-Charts/src")
from ewma import EWMA


def control_chart(df, x, y, center, lower, upper, title="Control Chart", font_size=None):
    fig = px.line(df, x=x, y=y, title=title)
    fig.add_trace(go.Scatter(x=df[x], y=df[center], mode="lines", showlegend=False, name="Center"))
    fig.add_trace(go.Scatter(x=df[x], y=df[lower], mode="lines", showlegend=False, name="Lower"))
    fig.add_trace(go.Scatter(x=df[x], y=df[upper], mode="lines", showlegend=False, name="Upper"))
    fig.update_layout(font=dict(size=font_size))
    plot(fig, filename=f"{title}.html")


data = pd.read_csv("/home/nick/Control-Charts/test/traffic.txt", sep="\t")

df = EWMA(x=data["Vehicles"].tolist(), alpha=0.1)

control_chart(
    df, 
    x="Observation", 
    y="EWMA", 
    center="EWMA CL",
    lower="EWMA LCL",
    upper="EWMA UCL",
    title="EWMA Chart",
)
