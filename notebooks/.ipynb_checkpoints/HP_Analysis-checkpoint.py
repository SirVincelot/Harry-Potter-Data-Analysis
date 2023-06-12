# Streamlit live coding script
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy
from plotly.subplots import make_subplots

# First some Data Exploration
@st.cache_data
def load_data(path):
    df = pd.read_csv(path, sep=";")
    return df


hp_df_raw = load_data(path="../data/Characters.csv")
hp_df = deepcopy(hp_df_raw)

hp_colors = color_list = ['#740001', '#ae0001', '#eeba30', '#d3a625', '#5d5d5d', '#aaaaaa', '#0e1a40', '#bebebe', '#946b2d', '#ecb939', '#f0c75e', '#726255', '#372e29']

# Add title and header
st.title("Introduction to Streamlit")
st.header("My Harry Potter Steamlit App")

# Widgets: checkbox (you can replace st.xx with st.sidebar.xx)
if st.checkbox("Show Entire Dataframe"):
    st.subheader("This is my dataset:")
    st.dataframe(data=hp_df)

# Setting up columns
left_column, middle_column, right_column = st.columns([3, 1, 1])

#House Distribution
house_df1 = hp_df.House.value_counts().reset_index()
#st.dataframe(data = house_df1)

house_df1 = house_df1.rename(columns = {"index" : "Houses", "House":"Count"})
house_fig = make_subplots(
    rows=1, cols=3,subplot_titles=(
        "House Distribution in Howgwarts",
        "Title2", 
        "Title3"
    )
)
house_fig.add_trace(go.Bar (x = house_df1["Houses"], y = house_df1["Count"]), row = 1, col = 1)
st.plotly_chart(house_fig)

loyalty_df = hp_df[["Name", "House", "Blood status", "Loyalty"]]


# Widgets: selectbox
houses = pd.unique(hp_df['House'])
selectedhouse = left_column.selectbox("Choose a House", houses)
if st.checkbox("Show Students"):
	st.dataframe(data=hp_df[hp_df["House"] == selectedhouse])

house_df = hp_df[hp_df.House == selectedhouse]
gender_df = house_df.groupby(by = "Gender")["Name"].count().reset_index()
gender_df.columns = ["Gender", "Count"]

profession_df = house_df.groupby(by = "Job")["Name"].count().reset_index()
profession_df.columns = ["Profession", "Count"]

blood_df = house_df.groupby(by = "Blood status")["Name"].count().reset_index()
blood_df.columns = ["Blood Status", "Count"]
#st.dataframe(gender_df)

fig = make_subplots(
    rows=2, cols=2,

    subplot_titles=(
        "Gender Distribution of people from this house",
        "Profession of people", 
        "Blood Status"
    )
)
fig.update_layout(height=800)

fig.add_trace(go.Bar (x = gender_df["Gender"], y = gender_df["Count"]), row = 1, col = 1)

fig.add_trace(go.Bar (x = profession_df["Profession"], y = profession_df["Count"]),
row = 1, col = 2)

fig.add_trace(go.Bar (x = blood_df["Blood Status"], y = blood_df["Count"]),
			  row = 2, col = 1)

st.plotly_chart(fig)