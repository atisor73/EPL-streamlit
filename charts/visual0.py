import altair as alt
import pandas as pd
import numpy as np


def chart_heatmap_timeline(df_team, df_rankings):
    df = df_team.merge(df_rankings[['team', 'rank']], how='left', on='team')

    # Sort by team and date, then assign game number
    df_team['game_num'] = df_team.sort_values(['team', 'date']).groupby('team').cumcount() + 1  # nth game, 1-indexed

        # Ensure 'date' is datetime
    df['date'] = pd.to_datetime(df['date'])

    # Optional: get latest rank for each team if you have a separate ranking dataframe
    # For now we’ll sort by team name alphabetically
    teams_sorted = df.sort_values(by='rank')['team']

    # Define color scale for results
    result_color = alt.Scale(
        domain=["win", "draw", "loss"],
        range=["#009E60", "#cacaca", "#FF4433"]
    )

    # Build heatmap
    heatmap = alt.Chart(df_team).mark_rect(height=22, width=15, opacity=0.9).encode(
        # x=alt.X('date:T', title='Date'),
        x=alt.X('game_num:O', title='Game #'),
        y=alt.Y('team:N',
                sort=teams_sorted,  # or sort by rank
                title='Team'),
        color=alt.Color('result:N', scale=result_color, legend=alt.Legend(title="Result")),
        tooltip=['team','opponent','venue','date', 'result', 'goals_for', 'goals_against']  # optional extra info
    ).properties(
        width=800,
        height=550
    )

    return heatmap



#### VISUAL 1
def chart_heatmap_table_summary(df_rankings):
    df = df_rankings

    team_order = (df.sort_values('rank')['team'].tolist())
    metric_order = ["goals_for", "goals_against", "goal_diff"]

    df["team_label"] = "Rank " + df["rank"].astype(int).astype(str) + ". " + df["team"]
    df['%_matches_won'] = np.round(df['%_matches_won'], 0)

    # Melt dataframe for Altair
    df_melt = df.melt(
        id_vars=["team_label", "rank"],
        value_vars=["rank", "goals_for", "goals_against", "goal_diff", '%_matches_won'],
        var_name="stat",
        value_name="value"
    )
    df_melt['value_label'] = df_melt.apply(
        lambda row: f"{int(row['value'])}%" if row['stat'] == '%_matches_won' else str(int(row['value'])),
        axis=1
    )

    # Sort teams by rank
    df_melt["team_label"] = pd.Categorical(df_melt["team_label"], 
                                    categories=df.sort_values("rank")["team_label"], 
                                    ordered=True)

    # Create heatmap
    heatmap = alt.Chart(df_melt).mark_rect().encode(
        x=alt.X('stat:N', title=None, sort=metric_order, axis=alt.Axis(labelAngle=0, orient='top')),
        y=alt.Y('team_label:N', title=None, sort=team_order, axis=alt.Axis(labelLimit=500, labelFontSize=12)),
        color=alt.Color('value:Q', 
                        scale=alt.Scale(scheme='magma', reverse=True, domain=[-70, 120],),  # or 'reds', 'blues'
                        legend=None),
        tooltip=['team_label', 'stat', 'value']
    )

    # Overlay text
    text = alt.Chart(df_melt).mark_text(baseline='middle', fontSize=12).encode(
        x=alt.X('stat:N', sort=metric_order, axis=alt.Axis(labelAngle=0, orient='top')),
        y=alt.Y('team_label:N', sort=team_order, axis=alt.Axis(labelLimit=500, labelFontSize=12)),
        text='value_label:N',
        color=alt.value('#cacaca')
    )

    final_chart = (heatmap + text).properties(width=750, height=500).configure_text(
        font='Courier'
    ).configure_axis(
        labelFont='Courier',
        titleFont='Courier'
    )

    return final_chart




def chart_heatmap_table_discipline(df_rankings, df_team):
    # Aggregate stats per team
    df_agg = df_team.groupby('team').agg(
        fouls=('fouls', 'sum'),
        yellows=('yellow', 'sum'),
        reds=('red', 'sum')
    ).reset_index()

    df = df_agg.merge(df_rankings, on='team')

    df["team_label"] = (
        "Rank "
        + df["rank"].astype(int).astype(str)
        + ". "
        + df["team"]
    )

    # Melt for Altair
    df_melt = df.melt(
        id_vars=["team_label", "rank"],
        value_vars=["fouls", "yellows", "reds"],
        var_name="stat",
        value_name="value"
    )

    # Normalize values per team (row) for color scaling
    df_melt['col_max'] = df_melt.groupby('stat')['value'].transform('max')
    df_melt['value_norm'] = df_melt['value'] / df_melt['col_max']

    # Add formatted label
    df_melt['value_label'] = df_melt['value'].astype(int).astype(str)

    # Team and metric order
    team_order = (df.sort_values('rank')['team_label'].tolist())
    metric_order = ['fouls', 'yellows', 'reds']

    # Heatmap with normalized color per row
    heatmap = alt.Chart(df_melt).mark_rect().encode(
        x=alt.X('stat:N', title=None, sort=metric_order, axis=alt.Axis(labelAngle=0, orient='top')),
        y=alt.Y('team_label:N', title=None, sort=team_order, axis=alt.Axis(labelLimit=500, labelFontSize=12)),
        color=alt.Color('value_norm:Q',
                        scale=alt.Scale(scheme='reds', reverse=False, domain=[0, 1]),
                        legend=None),
        tooltip=['team_label', 'stat', 'value']
    )

    # Text overlay
    text = alt.Chart(df_melt).mark_text(baseline='middle', fontSize=12).encode(
        x=alt.X('stat:N', sort=metric_order),
        y=alt.Y('team_label:N', sort=team_order, axis=alt.Axis(labelLimit=500, labelFontSize=12)),
        text='value_label:N',
        color=alt.value('#cacaca')
    )

    # Combine
    final_chart = (heatmap + text).properties(width=750, height=500).configure_text(
        font='Courier'
    ).configure_axis(
        labelFont='Courier',
        titleFont='Courier'
    )

    return final_chart