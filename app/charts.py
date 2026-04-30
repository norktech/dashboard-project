import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

DARK_BG = "#161b22"
PAPER_BG = "#0d1117"
ACCENT = "#00d4ff"
GRID_COLOR = "#30363d"

LAYOUT_BASE = dict(
    plot_bgcolor=DARK_BG,
    paper_bgcolor=PAPER_BG,
    font=dict(color="#c9d1d9", size=12),
    margin=dict(t=40, b=40, l=40, r=40),
    xaxis=dict(gridcolor=GRID_COLOR, zeroline=False),
    yaxis=dict(gridcolor=GRID_COLOR, zeroline=False)
)

def price_histogram(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return _empty_chart("No data available")
    fig = px.histogram(
        df, x="price", nbins=20,
        color_discrete_sequence=[ACCENT],
        template="plotly_dark",
        labels={"price": "Price (£)", "count": "Books"}
    )
    fig.update_layout(**LAYOUT_BASE, showlegend=False)
    return fig

def rating_pie(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return _empty_chart("No data available")
    fig = px.pie(
        df, values="Count", names="Rating",
        color_discrete_sequence=px.colors.sequential.Blues_r,
        template="plotly_dark",
        hole=0.4
    )
    fig.update_layout(
        plot_bgcolor=DARK_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(color="#c9d1d9")
    )
    return fig

def top_expensive_bar(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return _empty_chart("No data available")
    fig = px.bar(
        df, x="price", y="title", orientation="h",
        color="price",
        color_continuous_scale="Blues",
        template="plotly_dark",
        labels={"price": "Price (£)", "title": ""}
    )
    fig.update_layout(
        **LAYOUT_BASE,
        showlegend=False,
        coloraxis_showscale=False
    )
    return fig

def price_trend_line(df: pd.DataFrame) -> go.Figure:
    if df.empty or len(df) < 2:
        return _empty_chart("Not enough data points for trend analysis")
    fig = px.line(
        df, x="Date", y="Average Price",
        color_discrete_sequence=[ACCENT],
        template="plotly_dark",
        markers=True,
        labels={"Average Price": "Average Price (£)"}
    )
    fig.update_layout(**LAYOUT_BASE)
    return fig

def _empty_chart(message: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=14, color="#8b949e")
    )
    fig.update_layout(
        plot_bgcolor=DARK_BG,
        paper_bgcolor=PAPER_BG,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    return fig