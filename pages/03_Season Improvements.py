import streamlit as st
import altair as alt
from utils.io import load_data

from charts.theme import base_theme
from charts.visual3 import process_rankings, chart_dotplot, chart_quadrant


st.set_page_config(page_title="English Premier League Dashboard", layout="wide")

alt.themes.register("project", base_theme)
alt.themes.enable("project")

df_match_1, df_match_2, df_team_1, df_team_2, df_rankings_1, df_rankings_2 = load_data()

df_rankings_delta = process_rankings(df_rankings_1, df_rankings_2)



st.title("English Premier League")
st.markdown("Season match visualization: S2023-2024, S2024-2025")

st.header("Season Rankings 2023-2024 & 2024-2025")

### Visual 3: Rankings & Goal differences
st.markdown("""
    We will next make a plot that looks at how the rankings changed from season 1 (2023-2024)\
     to season 2 (2024-2025), and a separate scatterplot that looks at how rankings change with \
     goals scored for each team (`goals_for`). We can look for a positive correlation between \
     goals scored and improved rankings.
""")

st.altair_chart(
    chart_dotplot(df_rankings_delta),
    use_container_width=False
)


st.markdown("""
    Teams that fall above the diagonal did better in the second season and improved. \
    Teams that fall below the diagonal dropped in rankings. The improvement in rank is \
    represented by the length of the line. Tottenham dropped from rank 5 to 17, Nottm Forest\
     rose from rank 17 to 7 , Liverpool and Man City traded in 1st and 3rd place.

    In the goals vs. rankings plot, we see some positive correlation between goals scored and \
    team rank. Teams like New Castle, Chelsea, Wolves, and Everton had higher rankings despite \
    scoring less (seen by a negative slope). Arsenal scored less goals in the second season yet\
    maintained its ranking at number 2. Tottenham dropped 12 places, but scored only ten less \
    goals in the whole season.

    Upon clicking on each team, we can consider whether a drastic difference in goals scored \
    accompanies drastic changes in ranking. Similarly, Nott'm Forest improved by 10 rankings but \
    only scored 9 more goals. In contrast, Aston Villa scored 18 less goals but only dropped 2 rankings. 

    These findings may seem counterintuitive, but as we are only looking at how many goals each team \
    scored, and not how many were scored against them, some goals won't necessarily contribute to a change\
    in ranking. In ignoring/marginalizing over the `goals_against` values we are effectively looking at\
    all other teams' performances held equal relative to our team of interest.
""")


st.write("Now let's look at this more cleanly, specifically at the change in rankings and change in goals scored by each team.")

st.altair_chart(
    chart_quadrant(df_rankings_delta),
    use_container_width=False
)

st.markdown("""
    The green quadrants reflect the assumption that teams who score more goals in a new season will have higher rankings\
    (New Castle, Chelsea, Fulham) , \
    and those who score fewer goals will have lower rankings (Wolves, Everton). \
    We see six cases of teams who score more goals in a new season that\
    end up with lower rankings \
    (Man City, Aston Villa, West Ham, Man U, Tottenham, Crystal Palace), and conversely three cases where teams that \
    score fewer goals rise in rankings (Bournemouth, Brighton, Brentford). Liverpool is the only team who scored the \
    exact same number of goals between the two seasons (and had a +2 ranking).
""")
