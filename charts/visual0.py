import altair as alt
import pandas as pd
import numpy as np

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
        y=alt.Y('team_label:N', title=None, sort=team_order),
        color=alt.Color('value:Q', 
                        scale=alt.Scale(scheme='magma', reverse=True, domain=[-70, 120],),  # or 'reds', 'blues'
                        legend=None),
        tooltip=['team_label', 'stat', 'value']
    )

    # Overlay text
    text = alt.Chart(df_melt).mark_text(baseline='middle', fontSize=12).encode(
        x=alt.X('stat:N', sort=metric_order, axis=alt.Axis(labelAngle=0, orient='top')),
        y=alt.Y('team_label:N', sort=team_order),
        text='value_label:N',
        color=alt.value('#cacaca')
    )

    final_chart = (heatmap + text).properties(width=900, height=500).configure_text(
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
        y=alt.Y('team_label:N', title=None, sort=team_order),
        color=alt.Color('value_norm:Q',
                        scale=alt.Scale(scheme='reds', reverse=False, domain=[0, 1]),
                        legend=None),
        tooltip=['team_label', 'stat', 'value']
    )

    # Text overlay
    text = alt.Chart(df_melt).mark_text(baseline='middle', fontSize=12).encode(
        x=alt.X('stat:N', sort=metric_order),
        y=alt.Y('team_label:N', sort=team_order),
        text='value_label:N',
        color=alt.value('#cacaca')
    )

    # Combine
    final_chart = (heatmap + text).properties(width=900, height=500).configure_text(
        font='Courier'
    ).configure_axis(
        labelFont='Courier',
        titleFont='Courier'
    )

    return final_chart