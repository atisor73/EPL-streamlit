import altair as alt
import pandas as pd

def chart_mean_err_ref(df_match):
    # DATA CLEANING ---------------------------------------
    ref_summary = df_match.groupby('referee').agg(
        matches=('match_id','count'),
        avg_fouls=('total_fouls','mean'),
        std_fouls=('total_fouls','std'),
        avg_cards=('total_cards','mean'),
        std_cards=('total_cards','std')
    ).reset_index()

    ref_summary = ref_summary[ref_summary['matches'] >= 5]

    df_ref = df_match.merge(
        ref_summary[['referee', 'avg_fouls']],
        on='referee',
        how='inner'
    )

    # PLOTTING ERROR CHART ---------------------------------
    ref_select = alt.selection_point(name='ref_sel',fields=['referee'], on='click', empty='none')

    sort_ref = ref_summary.sort_values(by='avg_fouls', ascending=False)['referee'].values

    base = alt.Chart(ref_summary).encode(
        x=alt.X('avg_fouls:Q', title='Avg fouls per game'),
        y=alt.Y('referee:N', sort=sort_ref)
    )

    points = base.mark_circle(size=80, opacity=1.0).encode(
        color=alt.condition(ref_select, alt.value('darkorange'), alt.value('#565656')),
        tooltip=['avg_fouls']
    ).add_params(ref_select)

    errorbars = base.mark_errorbar(thickness=2, opacity=0.7).encode(
        x=alt.X('avg_fouls:Q', title='Avg fouls per game'),
        xError='std_fouls:Q',
        color=alt.condition(ref_select, alt.value('darkorange'), alt.value('#565656')),
        strokeWidth=alt.condition(ref_select, alt.value(2.5), alt.value(1.5))
    )

    jitter = alt.Chart(df_ref).mark_circle(
        size=20,
        opacity=0.9, color='lightgray'
    ).encode(
        x=alt.X('total_fouls:Q', title='Avg fouls per game'),
        y=alt.Y('referee:N', sort=sort_ref),
        # yOffset=alt.YOffset(
            # 'jitter:Q',
            # scale=alt.Scale(domain=[-0.1, 0.1])
    ).transform_calculate(
        jitter='random()'
    )

    ref_chart_err = (jitter + errorbars + points
        ).properties(width=350, height=500, title='Distribution of Fouls by Referee')


    # PLOTTING SCATTER ------------------------------------------------------
    title = alt.TitleParams(
        text={
            "expr": "ref_sel.referee ? 'Matches Officiated by ' + ref_sel.referee : 'Select a Referee'"
        }
    )
    ref_chart_scatter = alt.Chart(df_match, title=title).mark_circle(size=50).encode(
        x=alt.X('total_fouls:Q', title='Cards per Game'),
        y=alt.Y('total_cards:Q', title='Fouls per Game'),
        color=alt.condition(
            ref_select,
            alt.value('darkorange'),
            alt.value('lightgray')
        ),
        opacity=alt.condition(
            ref_select,
            alt.value(1),
            alt.value(0.4)
        ),
    ).properties(width=350, height=250,
    )

    final_chart = alt.hconcat(
        ref_chart_err,
        ref_chart_scatter
    ).resolve_scale(
        color='independent'
    )

    return final_chart



def chart_mean_err_team(df_team, df_rankings):

    team_fouls_summary = df_team.groupby('team').agg(
        matches=('match_id','count'),
        avg_fouls=('fouls','mean'),
        std_fouls=('fouls','std'),
        avg_cards=('cards','mean'),
        std_cards=('cards','std')
    ).reset_index()

    df_team_fouls = df_team.merge(
        team_fouls_summary[['team', 'avg_fouls']],
        on='team',
        how='left'
    )

    df_rankings = df_rankings.merge(team_fouls_summary[['team', 'avg_fouls']], on='team')


    # PLOTTING ERROR CHART ---------------------------------
    team_select = alt.selection_point(name='team_sel', fields=['team'], on='click', empty='none')

    sort_team = team_fouls_summary.sort_values(by='avg_fouls', ascending=False)['team'].values

    base = alt.Chart(team_fouls_summary).encode(
        x=alt.X('avg_fouls:Q', title='Avg fouls per game'),
        y=alt.Y('team:N', sort=sort_team)
    )

    points = base.mark_circle(size=80, opacity=1.0).encode(
        color=alt.condition(team_select, alt.value('darkorange'), alt.value('#565656')),
    ).add_params(team_select)

    errorbars = base.mark_errorbar(thickness=2, opacity=0.7).encode(
        x=alt.X('avg_fouls:Q', title='Avg fouls per game'),
        xError='std_fouls:Q',
        color=alt.condition(team_select, alt.value('darkorange'), alt.value('#565656')),
        strokeWidth=alt.condition(team_select, alt.value(2.5), alt.value(1.5)),
    )


    jitter = alt.Chart(df_team_fouls).mark_circle(
        size=20,
        opacity=0.9, color='lightgray'
    ).encode(
        x=alt.X('fouls:Q', title='Avg fouls per game'),
        y=alt.Y('team:N', sort=sort_team),
    ).transform_calculate(
        jitter='random()'
    )
    team_chart_err = (jitter + errorbars + points).properties(
        width=325, height=500, title='Distribution of Fouls by Team')


    # PLOTTING SCATTER ------------------------------------------------------
    df_team['total_fouls'] = df_team['fouls']
    df_team['total_cards'] = df_team['cards']

    title = alt.TitleParams(
        text={
            "expr": "team_sel.team ? 'Fouls and cards by' + team_sel.team : 'Select a Team'"
        }
    )
    # title = 'Average per team'
    team_chart_scatter = alt.Chart(df_team, title=title).mark_circle(size=50).encode(
        x=alt.X('total_fouls:Q', title='Cards per Game'),
        y=alt.Y('total_cards:Q', title='Fouls per Game'),
        color=alt.condition(
            team_select,
            alt.value('darkorange'),
            alt.value('lightgray')
        ),
        opacity=alt.condition(
            team_select,
            alt.value(1),
            alt.value(0.2)
        ),
        tooltip=['team', 'total_cards', 'total_fouls']
    ).properties(width=350, height=175,
    )

    # MAKE AVG FOULS BY TEAM RANK SCATTER CHART -----------
    chart_scatter_foul_rank = alt.Chart(df_rankings
        ).mark_circle(size=50
        ).encode(
        x='rank:N', y='avg_fouls',
        color=alt.condition(
            team_select,
            alt.value('darkorange'),
            alt.value('lightgray')
        )).properties(height=150, width=350, title='Ranking of Team & Avg Fouls')

    final_chart_team = alt.hconcat(
        team_chart_err,
        alt.vconcat(team_chart_scatter, chart_scatter_foul_rank)
    ).resolve_scale(
        color='independent'
    )

    return final_chart_team