import streamlit as st
import pandas as pd
import altair as alt

@st.cache_data
def process_rankings(df_rankings_1, df_rankings_2):
    d_rename_s1_suffix = {
        'rank':'rank_s1',
        'season_points':'season_points_s1',
        'goals_for':'goals_for_s1',
        'goals_against':'goals_against_s1',
        'goal_diff':'goal_diff_s1',
        'avg_fouls':'avg_fouls_s1',
    }
    d_rename_s2_suffix = {
        'rank':'rank_s2',
        'season_points':'season_points_s2',
        'goals_for':'goals_for_s2',
        'goals_against':'goals_against_s2',
        'goal_diff':'goal_diff_s2',
        'avg_fouls':'avg_fouls_s2',
    }

    df_rankings_delta = df_rankings_1.rename(columns=d_rename_s1_suffix
        ).merge(df_rankings_2.rename(columns=d_rename_s2_suffix), how='inner', on='team')

    df_rankings_delta['season_points_delta'] = df_rankings_delta['season_points_s1'] - df_rankings_delta['season_points_s2']
    df_rankings_delta['rank_delta'] = df_rankings_delta['rank_s1'] - df_rankings_delta['rank_s2']
    df_rankings_delta['goals_for_delta'] = df_rankings_delta['goals_for_s1'] - df_rankings_delta['goals_for_s2']
    df_rankings_delta['goals_against_delta'] = df_rankings_delta['goals_against_s1'] - df_rankings_delta['goals_against_s2']
    df_rankings_delta['goal_diff_delta'] = df_rankings_delta['goal_diff_s1'] - df_rankings_delta['goal_diff_s2']

    # for text later
    df_rankings_delta['rank_mid'] = (df_rankings_delta['rank_s1'] + df_rankings_delta['rank_s2']) / 2
    df_rankings_delta['rank_delta_text'] = df_rankings_delta['rank_delta'].map(lambda x: str(x) if x < 0 else '+' + str(x))
    df_rankings_delta['goals_for_delta_text'] = df_rankings_delta['goals_for_delta'].map(lambda x: str(x) if x < 0 else '+' + str(x))

    return df_rankings_delta

def chart_dotplot(df_rankings_delta):
    sorted_teams = df_rankings_delta.sort_values(by='rank_s2')['team'].to_list()

    # ----------- Selection on ranking plot
    team_select = alt.selection_point(fields=['team'], empty='none')

    base_rank = alt.Chart(df_rankings_delta).properties(
        title='Season 1 - 2 Ranking & Ranking Differences',
        width=320, height=450
    )

    color_scale = alt.Scale(domain=['season 1', 'season 2'], range=['slateblue', 'navy'])

    chart_s1_rank = base_rank.transform_calculate(
        season='"season 1"'
    ).mark_circle(size=80).encode(
        x=alt.X('rank_s1:Q', scale=alt.Scale(reverse=True)),
        y=alt.Y('team:N', sort=sorted_teams),
        color=alt.Color('season:N', scale=color_scale, legend=alt.Legend(title='Season')),
        tooltip=['team', 'rank_s1', 'rank_s2']
    )

    chart_s2_rank = base_rank.transform_calculate(
        season='"season 2"'
    ).mark_circle(size=80).encode(
        x=alt.X('rank_s2:Q', scale=alt.Scale(reverse=True)),
        y=alt.Y('team:N', sort=sorted_teams),
        color=alt.Color('season:N', scale=color_scale),
        tooltip=['team', 'rank_s1', 'rank_s2']
    )

    chart_line_rank = base_rank.mark_rule().encode(
        x='rank_s1:Q',
        x2='rank_s2:Q',
        y=alt.Y('team:N', sort=sorted_teams),
        color=alt.condition(team_select, alt.value('darkorange'), alt.value('#ababab')),
        strokeWidth=alt.condition(team_select, alt.value(2.5), alt.value(1.5)),
    )

    chart_diff = base_rank.mark_text(
        align='center', baseline='middle', dy=-7, fontSize=10, fontWeight='bold'
    ).encode(
        x='rank_mid:Q',
        y=alt.Y('team:N', sort=sorted_teams),
        text='rank_delta_text:N',
        color=alt.value('#565656')
    )

    ranking_chart = (chart_line_rank + chart_s1_rank + chart_s2_rank + chart_diff).add_params(team_select)  

    # ---------------- Bivariate plot (linked)
    base_bi = alt.Chart(df_rankings_delta).properties(
        title='Season 1 - 2 Goals scored & Rankings',
        width=400, height=400
    )

    # conditional color: grey if not selected, navy if selected
    chart_s1_bi = base_bi.transform_calculate(
        season='"season 1"'
    ).mark_circle(size=80).encode(
        y=alt.Y('rank_s1:Q', scale=alt.Scale(reverse=True)),
        x=alt.X('goals_for_s1:Q', scale=alt.Scale(reverse=False, zero=False)),
        color=alt.condition(team_select, alt.value('slateblue'), alt.value('#dddddd')),
        tooltip=['team', 'goals_for_s1', 'goals_for_s2', 'rank_s1','rank_s2']
    )

    chart_s2_bi = base_bi.transform_calculate(
        season='"season 2"'
    ).mark_circle(size=80).encode(
        y=alt.Y('rank_s2:Q', scale=alt.Scale(reverse=True)),
        x=alt.X('goals_for_s2:Q', scale=alt.Scale(reverse=False, zero=False)),
        color=alt.condition(team_select, alt.value('navy'), alt.value('#dddddd')),
        tooltip=['team', 'goals_for_s1', 'goals_for_s2', 'rank_s1','rank_s2']
    )

    chart_line_bi = base_bi.mark_line(color='#ababab').encode(
        y='rank_s1:Q',
        y2='rank_s2:Q',
        x='goals_for_s1:Q',
        x2='goals_for_s2:Q',
        color=alt.condition(team_select, alt.value('darkorange'), alt.value('#dddddd')),
        strokeWidth=alt.condition(team_select, alt.value(2.5), alt.value(1.5)),
        tooltip=['team', 'goals_for_s1', 'goals_for_s2', 'goals_for_delta_text', 'rank_s1','rank_s2', 'rank_delta_text'],
    )

    bivariate_chart = chart_line_bi + chart_s1_bi + chart_s2_bi

    # ------------ Display
    linked_charts = ranking_chart | bivariate_chart

    return linked_charts







def chart_quadrant(df_rankings_delta):
        # Quadrant polygons
    q1 = alt.Chart(pd.DataFrame([{'x_min':0,'x_max':df_rankings_delta['goals_for_delta'].max()*1.2,
                                'y_min':0,'y_max':df_rankings_delta['rank_delta'].max()*1.2}])
                ).mark_rect(color='green', opacity=0.2).encode(
                    x='x_min:Q',
                    x2='x_max:Q',
                    y='y_min:Q',
                    y2='y_max:Q'
                )

    # Q3: x<0, y<0
    q3 = alt.Chart(pd.DataFrame([{'x_min':df_rankings_delta['goals_for_delta'].min()*1.2,'x_max':0,
                                'y_min':df_rankings_delta['rank_delta'].min()*1.2,'y_max':0}])
                ).mark_rect(color='green', opacity=0.2).encode(
                    x='x_min:Q',
                    x2='x_max:Q',
                    y='y_min:Q',
                    y2='y_max:Q'
                )

    # Base scatter plot
    circle_chart = alt.Chart(df_rankings_delta).mark_circle(size=80, color='navy').encode(
        x=alt.X('goals_for_delta:Q', title='Goals For Δ'),
        y=alt.Y('rank_delta:Q', title='Rank Δ'),
        # color=alt.Color('rank_delta:Q',
        #                 scale=alt.Scale(scheme='redblue', domainMid=0),
        #                 legend=alt.Legend(title="Rank Δ")),
        tooltip=[
            alt.Tooltip('team:N', title='Team'),
            alt.Tooltip('rank_delta_text:N', title='Rank Δ'),
            alt.Tooltip('goals_for_delta_text:N', title='Goals Δ')
        ]
    ).properties(
        width=600,
        height=600,
        title="Goals For Delta vs Rank Delta"
    )

    # Reference lines at 0
    hline = alt.Chart(pd.DataFrame({'y':[0]})).mark_rule(color='#898989', strokeDash=[4,2]).encode(y='y:Q')
    vline = alt.Chart(pd.DataFrame({'x':[0]})).mark_rule(color='#898989', strokeDash=[4,2]).encode(x='x:Q')

    # Text labels near points
    labels = alt.Chart(df_rankings_delta).mark_text(
        align='left',
        dx=-15,  # shift right
        dy=-15, # shift up
        fontSize=12
    ).encode(
        x='goals_for_delta:Q',
        y='rank_delta:Q',
        text='team:N'
    )

    # Combine chart + reference lines
    final_chart = q1 + q3 + circle_chart + hline + vline + labels

    return final_chart