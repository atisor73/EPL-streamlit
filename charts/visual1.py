import altair as alt
import pandas as pd

#### VISUAL 1
def chart_heatmap(df_match, df_team, df_rankings):
    # Define selection
    selection = alt.selection_point(
        fields =['match_id'],
        on='click',
        empty=False
    )

    # ---------------- CREATE HEATMAP ---------------------
    team_order = (df_rankings.sort_values('rank')['team'].tolist())

    heatmap_base = alt.Chart(df_match, title='Goal difference (home - away)').mark_rect().encode(
        y=alt.Y('home_team:N', sort=team_order, axis=alt.Axis(labels=True)), 
        x=alt.X('away_team:N', sort=team_order), 
        color=alt.Color('goal_diff:Q', scale=alt.Scale(scheme='redblue', zero=True)),
        # color=alt.Color('goal_diff:Q', scale=alt.Scale(
        #         domain=[df_match['goal_diff'].min(), 0, df_match['goal_diff'].max()], 
        #         range=['#b2182b', '#efefef', '#2166ac'], 
        #     )),
        tooltip=['home_team', 'away_team', 'goal_diff', 'goals_for', 'goals_against']
    )
    heatmap_highlight = heatmap_base.mark_rect(
        stroke='black',
        strokeWidth=3,
        fillOpacity=0,
    ).encode(
        opacity=alt.condition(selection, alt.value(1), alt.value(0))
    )

    # Add click
    heatmap = (heatmap_base + heatmap_highlight).add_params(selection).properties(
        width=390,
        height=400
    )




    # CREATE RUG
    # Melt dataframe
    df_long = df_team.melt(
        id_vars=['match_id','team', 'opponent'], 
        value_vars=['_shots_on_target_accuracy', 
                    '_goal_accuracy', 
                    'shots_on_target', 
                    '_discipline'],
        var_name='metric',
        value_name='value'
    ).rename(columns={'team':'home_team', 'opponent':'away_team'})

    # Define the dropdown or radio options
    metric_options = [
        '_shots_on_target_accuracy',
        '_goal_accuracy',
        'shots_on_target',
        '_discipline'
    ]
    # Define a selection bound to the dropdown (or radio)
    metric_selection = alt.param(
        name="metric",
        bind=alt.binding_radio(options=metric_options, name='Metric: '),
        value=metric_options[0]
    )

    # # Slider for tick width (thickness)
    width_slider = alt.binding_range(min=1, max=20, step=1, name='Width:')
    width_param = alt.param(value=4, bind=width_slider)

    # # Slider for tick width (thickness)
    opacity_slider = alt.binding_range(min=0.01, max=1.0, step=0.01, name='Opacity:')
    opacity_param = alt.param(value=0.2, bind=opacity_slider)

    title=alt.Title(alt.expr(f"{metric_selection.name}"))

    # Base rug chart
    rug_base = alt.Chart(df_long, title=title
        ).mark_tick(opacity=opacity_param,thickness=4, color='#232343'
        ).encode(
        x=alt.X('value:Q', axis=alt.Axis(grid=False)),
        y=alt.Y('home_team', sort=team_order),
    )
    rug_highlight = rug_base.mark_tick(stroke='darkorange', strokeWidth=6, fillOpacity=0).encode(
        opacity=alt.condition(selection, alt.value(1), alt.value(0))
    )

    rug = (rug_base + rug_highlight
        ).add_params(opacity_param,
        ).add_selection(
            metric_selection,
        ).transform_filter("datum.metric == metric"
        ).properties(
            width=275, height=400,
        )


    final_chart = alt.hconcat(heatmap, rug)

    # from IPython.display import HTML
    # display(HTML("""
    # <style>
    # .vega-bind {
    # text-align:right;
    # }
    # </style>
    # """))



    # Render the Altair chart
    return final_chart
