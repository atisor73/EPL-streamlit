import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

from utils.io import load_data
from charts.theme import base_theme
from charts.visual0 import chart_heatmap_table_summary, chart_heatmap_table_discipline


st.set_page_config(page_title="English Premier League Dashboard", layout="wide")
alt.themes.register("project", base_theme)
alt.themes.enable("project")

df_match_1, df_match_2, df_team_1, df_team_2, df_rankings_1, df_rankings_2 = load_data()


st.title("English Premier League")
st.markdown("Season match visualization: S2023-2024, S2024-2025")

st.write("This project is meant to serve as a demonstration of how Streamlit can be used \
    to deploy a web-app with interactive Altair charts. These solutions were created by \
    TA Rosita Fu as an example solution for HW4 for UChicago DATA227 Winter 2026. \n")

st.write("This is a fun voronoi tree-map I created using a d3 extension: \
    https://github.com/Kcnarf/d3-voronoi-map. The polygonal area of each team is \
    in theory proportional to the total number of goals they scored in a given season. \
    I did not fully integrate this into the streamlit workflow, and instead saved the results\
    in an `.svg` file."
)

# Centering widget
left, center, right = st.columns([1, 2, 1])

with center:
    season = st.segmented_control(
        "Select Season",
        ["Season 1", "Season 2"],
    )


if season == "Season 2":
    with open("images/voronoi_s2.svg", "r") as f:
        svg = f.read()
else:
    with open("images/voronoi_s1.svg", "r") as f:
        svg = f.read()

st.markdown(
    f"""
    <div style="display:flex; justify-content:center;">
        {svg}
    </div>
    """,
    unsafe_allow_html=True
)


# TEAM STATS --------------------------------------------------------------
st.header("Team Stats")

# --- Conditional rendering ---
if season == "Season 2":
    st.altair_chart(
        chart_heatmap_table_summary(df_rankings_2),
        use_container_width=False
    )
else:
    st.altair_chart(
        chart_heatmap_table_summary(df_rankings_1),
        use_container_width=False
    )

# FOUL STATS --------------------------------------------------------------
st.header("Foul Stats")

# --- Conditional rendering ---
if season == "Season 2":
    st.altair_chart(
        chart_heatmap_table_discipline(df_rankings_2, df_team_2),
        use_container_width=False
    )
else:
    st.altair_chart(
        chart_heatmap_table_discipline(df_rankings_1, df_team_1),
        use_container_width=False
    )
st.markdown("""
    We can see how the final rankings relate to the summary statistics computed over all matches, \
    as well as how aggressively a team plays a role in the final ranking. 
""")

st.write(
    "In the following sections we explore additional visuals through the pages in the sidebar:\n"
    "- **Performance timeline**: Visualize a team’s match results across the season.\n"
    "- **Goal differences**: Visualize individual match results and how goal differences relate to shot and goal accuracies.\n"
    "- **Foul distribution**: Compare distribution of fouls and cards by referees and teams.\n"
    "- **Season improvements**: Track how team rankings change from 2023-2024 to 2024-2025. \n"
)


