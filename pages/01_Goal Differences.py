import streamlit as st
import altair as alt
from utils.io import load_data

from charts.theme import base_theme
from charts.visual1 import chart_heatmap

# st.set_page_config(page_title="English Premier League Dashboard", layout="wide")

alt.themes.register("project", base_theme)
alt.themes.enable("project")

df_match_1, df_match_2, df_team_1, df_team_2, df_rankings_1, df_rankings_2 = load_data()


st.title("English Premier League")
st.markdown("Season match visualization: S2023-2024, S2024-2025")

st.header("Goal differences")
st.write("Let's create a visual to capture the goal difference across all matches in the season\
     using a heatmap, and link that to a chart to measure 'shot accuracy' of each match relative\
    to the distribution of each team.")

st.write("This allows us to see, in one view, what the distribution of goal differences are across\
     each home and away team, understand the season ranking (how the home team is sorted along the y-axis) \
     of a team, their goal difference distribution when playing at home (and inverted when away), and at a \
     match-level see where in the distribution of shot accuracy (shots on target or goal accuracy) this falls\
      for each team. We can see the distribution of each team's shot accuracy, and for a selected match linked \
      across plots, where in the distribution that falls. ")


## {Heatmap of goal difference} & {Rugplot of shot acc metric} for one season.
st.markdown("""
This allows us to answer the following questions:
- Do top-ranking teams have large goal differences, which may imply an aggressive strategy, or a \
    safer strategy that would lead to a smaller goal difference?
- Which teams have high shots-on-target or goal accuracies? How large is this variance across teams? (Rug plot)
- Do matches with large goal differences have high shot accuracies for the winning team? Or is \
    this more a function of many attempts? (Heatmap + Rug plot)
""")
# CHART ---------------------------------

# Optional: inject custom CSS
st.markdown(
    """
    <style>
    .vega-bind {
        text-align: right;
    }
    .sidebar .sidebar-content {{
                width: 375px;
            }}

    </style>
    """,
    unsafe_allow_html=True
)

# --- Radio toggle ---
season = st.radio(
    "Select Season",
    ["Season 1", "Season 2"],
    horizontal=True
)


# --- Conditional rendering ---
if season == "Season 1":
    st.altair_chart(
        chart_heatmap(df_match_1, df_team_1, df_rankings_1),
        use_container_width=False
    )
else:
    st.altair_chart(
        chart_heatmap(df_match_2, df_team_2, df_rankings_2),
        use_container_width=False
    )


# st.caption("Takeaway: Temperature fluctuates heavily day-to-day. There is evidence of strong seasonality and occasional extremes.")

st.markdown("""
This admittedly is quite an overwhelming dashboard, it's one of those seeing \
'everything, everywhere, all-at-once' type charts.

- The heatmap shows the distribution and consistency of wins and 'severity' of wins \
(intensity of color). In the first season, Man City has never lost a match when playing \
in their home venue, but when Man City was the away team, they lost 3 matches. 
- Liverpool, the third-ranking team, consistently had around a 1-3 goal difference. Liverpool \
and Tottenham both have relatively tame goal difference distributions relative to Man City and Arsenal.
- When clicking on each square, we can see whether outliers in matches with large goal \
differences were also outliers in shots-on-target accuracy or goal accuracy, or rather \
due to a higher volume of shots on target by toggling the metric below. For example, we \
see that in Man City v. Bournemouth, both teams had an average shots-on-target accuracy \
relative to their entire season performance, but both had really high goal accuracies \
relative to their individual season performance, but this is attributed to a lower volume \
of shots-on-target by Bournemouth. We can also see that Bournemouth had a higher volume of disciplines.


Overall, this gives a really quick snapshot of what happened in each match from a shot-on-target and \
goal accuracy and volume perspective, allowing us to evaluate the goal difference relative to all \
games in the season, and shots-on-target and goals relative to each team's seasonal performance, and\
 see how these metrics connect.
""")