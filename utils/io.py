import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df_match_1 = pd.read_csv("data/DF_MATCH_1.csv")
    df_match_2 = pd.read_csv("data/DF_MATCH_2.csv")
    df_team_1 = pd.read_csv("data/DF_TEAM_1.csv")
    df_team_2 = pd.read_csv("data/DF_TEAM_2.csv")
    df_rankings_1 = pd.read_csv("data/DF_RANKINGS_1.csv")
    df_rankings_2 = pd.read_csv("data/DF_RANKINGS_2.csv")

    return df_match_1, df_match_2, df_team_1, df_team_2, df_rankings_1, df_rankings_2


df_match_1, df_match_2, df_team_1, df_team_2, df_rankings_1, df_rankings_2 = load_data()