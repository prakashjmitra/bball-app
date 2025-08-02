import streamlit as st #Building web app
import pandas as pd #Webscraping
import base64 #Data download for the csv

'''
Libraries for heat plot
'''
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title("NBA Players Stats Explorer")

st.markdown("""This applicaton provides simple webscraping of NBA player stats data!
* **Python libraries: ** base64, pandas, streamlit
* **Data source: ** [basketball-reference.com](https://basketball-reference.com)
            """)

st.sidebar.header("User Inputs")
selected_year = st.sidebar.selectbox("Year",list(reversed(range(1950,2020))))

@st.cache #If the data has already been loaded, this will catch the data and the load data dosen't have to run again
def load_data(year):
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"
    html = pd.read_html(url, header = 0)
    df = html[0]
    raw = df.drop(df[df.Age == "Age"].index)
    raw = raw.fillna(0)
    playerstats = raw.drop(["Rk"], axis = 1)
    return playerstats
playerstats = load_data(selected_year)


#Team selection
sorted_unique_team = sorted(playerstats.T)
selected_team = st.sidebar.multiselect("Team", sorted_unique_team, sorted_unique_team) # Need to repeat values twice to include values

#Position Selection
sorted_unique_position = ["PG", "SG", "SF", "PF", "C"]
selected_position = st.sidebar.multiselect("Position", sorted_unique_position, sorted_unique_position)

df_selected_team = playerstats[(playerstats.T.isin(selected_team)) & (playerstats.Pos.isin(selected_position))]

st.header("Player Stats of Selected Team(s)")
st.write("Data Dimensions: " + str(df_selected_team.shape[0]) + "rows and " + str(df_selected_team.shape[1]) + "columns")
st.dataframe(df_selected_team)

#Download CSV file function
def filedownload(df):
    csv = df.to_csv(index = False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download ="playerstats.csv"> Download CSV File </a>'
    return href
st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

if st.button("Intercorrelation Heatmap"):
    st.header("Intercorrelation Heatmap")
    df_selected_team.to_csv("output.csv",index = False)
    df = pd.read_csv("output.csv")

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        fig, ax = plt.subplots(figsize=(7,5))
        ax = sns.heatmap(corr, mask=mask, vmax =1, square = True)
    st.pyplot()




