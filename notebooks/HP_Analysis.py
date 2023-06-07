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

#region import df
# First some Data Exploration
# @st.cache_data
def load_data(path):
    df = pd.read_csv(path, sep=";")
    return df


hp_df_raw = load_data(path="notebooks/Characters.csv")
hp_df = deepcopy(hp_df_raw)

hp_colors = color_list = ['#740001', '#ae0001', '#eeba30', '#d3a625', '#5d5d5d', '#aaaaaa', '#0e1a40', '#bebebe', '#946b2d', '#ecb939', '#f0c75e', '#726255', '#372e29']

# Add title and header
st.title("Introduction to Streamlit")
st.header("My Harry Potter Steamlit App")

#region Data cleaning


hp_df["Loyalty"] = hp_df["Loyalty"].fillna("Unknown")
hp_df["House"] = hp_df["House"].fillna("Unknown")
hp_df["Blood status"] = hp_df["Blood status"].fillna("Unknown")
hp_df["Job"] = hp_df["Job"].fillna("Unknown")
hp_df["Death"] = hp_df["Death"].fillna("Still Alive")

#show null values
#st.text(hp_df.isna().sum())

#region define loyalties

hp_df["Loyalty_Albus Dumbledore"] = hp_df["Loyalty"].apply(lambda x : 1 if "Albus Dumbledore" in x else 0)
hp_df["Loyalty_Order of the Phoenix"] = hp_df["Loyalty"].apply(lambda x : 1 if "Order of the Phoenix" in x else 0)
hp_df["Loyalty_Dumbledores Army"] = hp_df["Loyalty"].apply(lambda x : 1 if "Dumbledore's Army" in x else 0)
hp_df["Loyalty_Hogwarts"] = hp_df["Loyalty"].apply(lambda x : 1 if "Hogwarts School of Witchcraft and Wizardry" in x else 0)
hp_df["Loyalty_Voldemort"] = hp_df["Loyalty"].apply(lambda x : 1 if "Lord Voldemort" in x else 0)
hp_df["Loyalty_Death Eaters"] = hp_df["Loyalty"].apply(lambda x : 1 if "Death Eaters" in x else 0)
hp_df["Loyalty_Gringotts"] = hp_df["Loyalty"].apply(lambda x : 1 if "Gringotts Wizarding Bank" in x else 0)
hp_df["Loyalty_Unknown"] = hp_df["Loyalty"].apply(lambda x : 1 if "Unknown" in x else 0)

hp_df["Loyalty_Ministry of Magic"] = hp_df["Loyalty"].apply(lambda x : 1 if "Ministry of Magic" in x else 0)
hp_df["Loyalty_Ministry of Magic"] = hp_df["Loyalty"].apply(lambda x : 1 if "Minister of Magic" in x else 0)
hp_df["Loyalty_Grindelwald"] = hp_df["Loyalty"].apply(lambda x : 1 if "Gellert Grindelwald" in x else 0)

loyalties_true = ["Loyalty_Albus Dumbledore", "Loyalty_Order of the Phoenix", "Loyalty_Dumbledores Army", "Loyalty_Hogwarts", "Loyalty_Voldemort",
                                               "Loyalty_Death Eaters", "Loyalty_Gringotts", "Loyalty_Unknown", "Loyalty_Ministry of Magic", "Loyalty_Grindelwald"]
#endregion

#region good vs evil
good = ["Albus Dumbledore", "Order of the Phoenix", "Dumbledores Army", "Dumbledore's Army", "Hogwarts"]
neutral = ["Gringotts", "Unknown", "Ministry of Magic", "Minister of Magic"] 
evil = ["Voldemort","Death Eaters", "Grindelwald"]

spirits = ["good", "neutral", "evil"]

def findevil(loyalty):
    spirit = ""
    for spir in good:
        if spir in loyalty:
            spirit = "good"  
    for spir in neutral:
        if spir in loyalty:
            spirit = "neutral"  
    for spir in evil:
        if spir in loyalty:
            spirit = "evil"     
    return spirit

hp_df["Spirit"] = hp_df.Loyalty.apply(lambda x : findevil(x))
#endregion

# region dead?
hp_df["Dead"] = hp_df["Death"].apply(lambda x : "Dead" if x != "Still Alive" else "Alive")
#endregion


#endregion

# Widgets: checkbox (you can replace st.xx with st.sidebar.xx)
if st.checkbox("Show Entire Dataframe"):
    st.subheader("This is my dataset:")
    st.dataframe(data=hp_df)

# Setting up columns
left_column, middle_column, right_column = st.columns([3, 1, 1])
#endregion

house_fig = go.Figure(data = go.Bar())

#region Gender House Distribution
gender_by_house_df = hp_df.groupby(by = ["House", "Gender"]).Name.count().reset_index()

house_fig.add_trace(go.Bar (x = gender_by_house_df[gender_by_house_df.Gender == "Male"].House, y =gender_by_house_df[gender_by_house_df.Gender == "Male"].Name, name = "Male"))
house_fig.add_trace(go.Bar (x = gender_by_house_df[gender_by_house_df.Gender == "Female"].House, y = gender_by_house_df[gender_by_house_df.Gender == "Female"].Name, name = "Female"))

house_fig.update_layout(barmode = "stack", title = "Gender per House", xaxis_title = "Houses", yaxis_title= "People in Howgwarts")
st.plotly_chart(house_fig)
#endregion

#region house by spirit
spirit_house_fig = go.Figure(data = go.Bar())

spirit_house_df = hp_df.groupby(by = ["Spirit", "House"]).Name.count().reset_index()

house_colors = ['#FF0000', '#FFD700', '#0000FF', '#008000']

spirit_house_fig.add_trace(go.Bar (x = spirit_house_df[spirit_house_df.House == "Gryffindor"].Spirit, y = spirit_house_df[spirit_house_df.House == "Gryffindor"]["Name"],                                  name = "Gryffindor", marker=dict(color="#FF0000")))
spirit_house_fig.add_trace(go.Bar (x = spirit_house_df[spirit_house_df.House == "Hufflepuff"].Spirit, y = spirit_house_df[spirit_house_df.House == "Hufflepuff"]["Name"],                                    name = "Hufflepuff", marker=dict(color="#FFD700")))
spirit_house_fig.add_trace(go.Bar (x = spirit_house_df[spirit_house_df.House == "Ravenclaw"].Spirit, y = spirit_house_df[spirit_house_df.House == "Ravenclaw"]["Name"],                                     name = "Ravenclaw", marker=dict(color="#0000FF")))
spirit_house_fig.add_trace(go.Bar (x = spirit_house_df[spirit_house_df.House == "Slytherin"].Spirit, y = spirit_house_df[spirit_house_df.House == "Slytherin"]["Name"],  
                                   name = "Slytherin", marker=dict(color="#008000")))

spirit_house_fig.update_layout(barmode = "stack", title = "Good vs Evil per House", xaxis_title = "Spirit", yaxis_title= "People in Howgwarts")

st.plotly_chart(spirit_house_fig)
#endregion

#region loyality by house
loy_fig = go.Figure(data = go.Bar())

for loy in loyalties_true:
    loyalty_by_house_df = hp_df.groupby(by = ["House", loy]).Name.count().reset_index()
    loyalty_by_house_df = loyalty_by_house_df[loyalty_by_house_df[loy] == 1]
    #st.dataframe(loyalties_dict["Loyalty_Hogwarts"])
    loy_fig.add_trace(go.Bar (x = loyalty_by_house_df["House"], y = loyalty_by_house_df["Name"],  name = loy))

loy_fig.update_layout(barmode = "stack", title = "Loyalties per House", xaxis_title = "Houses", yaxis_title= "People in Howgwarts")
st.plotly_chart(loy_fig)
#endregion


#region discover by house
# Widgets: selectbox
houses = pd.unique(hp_df['House'])
selectedhouse = st.selectbox("Choose a House", houses)
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
#endregion



#region death by spirit
spirit_fig = go.Figure(data = go.Bar())

spirit_df = hp_df.groupby(by = ["Spirit", "Dead"]).Name.count().reset_index()
st.dataframe(spirit_df)

spirit_fig.add_trace(go.Bar (x = spirit_df[spirit_df.Dead == "Dead"].Spirit, y = spirit_df[spirit_df.Dead == "Dead"]["Name"],  name = "Dead"))
spirit_fig.add_trace(go.Bar (x = spirit_df[spirit_df.Dead == "Alive"].Spirit, y = spirit_df[spirit_df.Dead == "Alive"]["Name"],  name = "Alive"))

spirit_fig.update_layout(barmode = "stack", title = "Deaths per Spirit", xaxis_title = "Spirit", yaxis_title= "People in Howgwarts")
st.plotly_chart(spirit_fig)
#endregion


