"""Interactive SpaceX launch-site dashboard for the IBM Data Science Capstone."""

from pathlib import Path

import dash
from dash import Input, Output, dcc, html
import pandas as pd
import plotly.express as px


DATA_PATH = Path(__file__).with_name("spacex_launch_dash.csv")
spacex_df = pd.read_csv(DATA_PATH)

MIN_PAYLOAD = float(spacex_df["Payload Mass (kg)"].min())
MAX_PAYLOAD = float(spacex_df["Payload Mass (kg)"].max())
SITE_OPTIONS = [
    {"label": site, "value": site}
    for site in sorted(spacex_df["Launch Site"].unique())
]


app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    [
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#17365D"},
        ),
        html.P(
            "Compare landing outcomes by launch site and explore the relationship "
            "between payload mass, booster family and landing class."
        ),
        dcc.Dropdown(
            id="site-dropdown",
            options=[{"label": "All Sites", "value": "ALL"}, *SITE_OPTIONS],
            value="ALL",
            clearable=False,
            searchable=True,
        ),
        dcc.Graph(id="success-pie-chart"),
        html.P("Payload range (kg)"),
        dcc.RangeSlider(
            id="payload-slider",
            min=MIN_PAYLOAD,
            max=MAX_PAYLOAD,
            step=500,
            marks={
                int(value): f"{int(value):,}"
                for value in range(int(MIN_PAYLOAD), int(MAX_PAYLOAD) + 1, 2500)
            },
            value=[MIN_PAYLOAD, MAX_PAYLOAD],
            tooltip={"placement": "bottom", "always_visible": False},
        ),
        dcc.Graph(id="success-payload-scatter-chart"),
    ],
    style={
        "maxWidth": "1100px",
        "margin": "0 auto",
        "padding": "24px",
        "fontFamily": "Arial, sans-serif",
    },
)


@app.callback(
    Output("success-pie-chart", "figure"),
    Output("success-payload-scatter-chart", "figure"),
    Input("site-dropdown", "value"),
    Input("payload-slider", "value"),
)
def update_dashboard(selected_site, payload_range):
    """Return the site-level pie chart and payload-filtered scatter plot."""
    low_payload, high_payload = payload_range

    if selected_site == "ALL":
        successful = spacex_df.loc[spacex_df["class"] == 1]
        pie = px.pie(
            successful,
            names="Launch Site",
            title="Share of successful launches by site",
            color_discrete_sequence=px.colors.qualitative.Safe,
        )
        site_frame = spacex_df
    else:
        site_frame = spacex_df.loc[spacex_df["Launch Site"] == selected_site]
        outcome_counts = (
            site_frame["class"]
            .value_counts()
            .rename_axis("class")
            .reset_index(name="launches")
        )
        outcome_counts["outcome"] = outcome_counts["class"].map(
            {0: "Unsuccessful", 1: "Successful"}
        )
        pie = px.pie(
            outcome_counts,
            values="launches",
            names="outcome",
            title=f"Landing outcomes at {selected_site}",
            color="outcome",
            color_discrete_map={"Successful": "#2E8B57", "Unsuccessful": "#C94C4C"},
        )

    filtered = site_frame.loc[
        site_frame["Payload Mass (kg)"].between(low_payload, high_payload)
    ].copy()
    filtered["Outcome"] = filtered["class"].map({0: "Failure", 1: "Success"})

    scatter = px.scatter(
        filtered,
        x="Payload Mass (kg)",
        y="class",
        color="Booster Version Category",
        symbol="Outcome",
        hover_data=["Launch Site", "Flight Number", "Booster Version"],
        title=f"Payload and landing outcome ({low_payload:,.0f}-{high_payload:,.0f} kg)",
        labels={"class": "Landing class (0 = failure, 1 = success)"},
    )
    scatter.update_yaxes(tickmode="array", tickvals=[0, 1])

    return pie, scatter


if __name__ == "__main__":
    app.run(debug=True)
