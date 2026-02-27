import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np


st.set_page_config(page_title="English Premier League Dashboard", layout="wide")

st.title("English Premier League")
st.write("This project is meant to serve as a demonstration of how Streamlit can be used \
    to deploy a web-app with interactive Altair charts. These solutions were created by \
    Rosita Fu as an example solution for HW4 for UChicago DATA227 for the Winter 2026 quarter. \n")
st.write(
    "Navigate visuals through the pages in the sidebar:\n"
    "- **Goal differences**: Match view.\n"
    "- **Foul distribution**: Distribution of fouls and cards by referees and teams.\n"
    "- **Season improvements**: We visualize how season rankings change from 2023-2024 to 2024-2025. \n"
)
# st.info("Dataset: `vega_datasets.data.seattle_weather()`")

# x = st.slider("Select a number", 0, 100, 50)
# st.write("You selected:", x)

# df = pd.DataFrame(
#     np.random.randn(20, 3),
#     columns=["A", "B", "C"]
# )

# st.line_chart(df)