import streamlit as st
import altair as alt
from utils.io import load_data

from charts.theme import base_theme
from charts.visual0 import chart_heatmap_timeline

# st.set_page_config(page_title="English Premier League Dashboard", layout="wide")

alt.themes.register("project", base_theme)
alt.themes.enable("project")

df_match_1, df_match_2, df_team_1, df_team_2, df_rankings_1, df_rankings_2 = load_data()

st.title("English Premier League")
st.markdown("Season match visualization: S2023-2024, S2024-2025")



# --- Radio toggle ---
season = st.radio(
    "Select Season",
    ["Season 1", "Season 2"],
    horizontal=True,
    key='season_ref',
)

# TEAM OVERVIEW --------------------------------------------------------------
st.header("Performance Timeline")

st.markdown(""" We visualize each team’s season as a timeline of matches, with \
each game colored by its result. This makes it easy to spot streaks and visualize \
the distribution of wins, draws, and losses over time. In the next tab, we will visualize individual match results.

""")

# --- Conditional rendering ---
if season == "Season 2":
    st.altair_chart(
        chart_heatmap_timeline(df_team_2, df_rankings_2),
        use_container_width=False
    )
else:
    st.altair_chart(
        chart_heatmap_timeline(df_team_1, df_rankings_1),
        use_container_width=False
    )
