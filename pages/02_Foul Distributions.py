import streamlit as st
import altair as alt
from utils.io import load_data

from charts.theme import base_theme
from charts.visual2 import chart_mean_err_ref, chart_mean_err_team


st.set_page_config(page_title="English Premier League Dashboard", layout="wide")


alt.themes.register("project", base_theme)
alt.themes.enable("project")

df_match_1, df_match_2, df_team_1, df_team_2, df_rankings_1, df_rankings_2 = load_data()



st.title("English Premier League")
st.markdown("Season match visualization: S2023-2024, S2024-2025")

st.header("Foul distributions by Referee")
st.write("In the next visual we will look at the distribution of fouls by referee \
and the correlation between fouls and cards when selected by referee. This visual \
will reveal any outliers in referee behavior, and show the fouling and carding consistency\
 in referee behavior across the season.\n \
  We will then generate the same view for each team and see whether certain teams are outliers \
  in receiving fouls/cards. ")



# --- Radio toggle ---
season_ref = st.radio(
    "Select Season",
    ["Season 1", "Season 2"],
    horizontal=True,
    key='season_ref',
)

# --- Conditional rendering ---
if season_ref == "Season 2":
    st.altair_chart(
        chart_mean_err_ref(df_match_2),
        use_container_width=False
    )
else:
    st.altair_chart(
        chart_mean_err_ref(df_match_1),
        use_container_width=False
    )

st.markdown("""
    Across both seasons, D. Coote consistently appears in the top three for average fouls distributed per match.\
    In the first season, G Scott is generally more lenient, with an average of 17.5 fouls per game,\
     with all other refs averaging between 20-25. The refs with the narrowest distributions \
     in count are T Bramall and T Harrington. Because different refs oversee a different number\
      of games, it's hard to compare their distributions. Generally speaking, referees like\
       A Taylor, M Oliver, A Madley, S Hooper, P Tierney  have high variance in both fouls \
       and cards per game with enough data points to make these metrics robust and interpretable. \n\
    Additionally, we see a slight correlation with fouls and cards per game, i.e. matches with high \
    cards tend to also have many fouls, and there tend to be way more cards than fouls per game.
""")

# ------------------------------------- NOW BY TEAM ------------------------------------------
st.header("Foul distributions by Team")
# --- Radio toggle ---
season_team = st.radio(
    "Select Season",
    ["Season 1", "Season 2"],
    horizontal=True,
    key="season_team"
)


# --- Conditional rendering ---
if season_team == "Season 2":
    st.altair_chart(
        chart_mean_err_team(df_team_2, df_rankings_2),
        use_container_width=False
    )
else:
    st.altair_chart(
        chart_mean_err_team(df_team_1, df_rankings_1),
        use_container_width=False
    )


st.write("""
    In both seasons, Man City had the lowest average number of fouls per game and sits low in the \
    distribution for cards per game as well, while Bournemouth has the highest number \
    of fouls. We also look at whether or not there is a trend with the average number of \
    fouls and the rank of a team. There is not a very discernible pattern. 
""")


st.write("""
   From the two sets of plots, it seems that the distribution is 10-13 fouls per match per team,\
    referees give 20-25 fouls per match. The distributions for both are well matched, given that\
     the referee fouls are counted across two teams per match.
""")

