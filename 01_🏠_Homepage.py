# --- LIBRARIES ---
import folium
import requests
import pandas as pd
import altair as alt

import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_folium import st_folium

# Set up the configuration of the webpage
app_title = "Bowling League"

# --- STORING ASSETS ---
def load_animation(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

animation_bowling_1 = load_animation("https://assets10.lottiefiles.com/datafiles/qbAoVVjPqpGHkwP/data.json")
animation_bowling_2 = load_animation("https://assets10.lottiefiles.com/private_files/lf30_rivr2ir4.json")

# --- CONNECTING AND LOADING DATA ---
url_location = "https://raw.githubusercontent.com/P33Rview/Bowling_league_app/master/datasets/LOCATION.csv"
url_win_points = "https://raw.githubusercontent.com/P33Rview/Bowling_league_app/master/datasets/SPARE_STRIKE.csv"

dataframe_location = pd.read_csv(url_location)
dataframe_win_points = pd.read_csv(url_win_points)

# DATAFRAMES
df_location = pd.DataFrame(dataframe_location)
df_win_points = pd.DataFrame(dataframe_win_points)

#subheaders showing the season list
seasons = df_win_points.season.unique()
season_list = (', '.join(seasons))

def main():
    st.set_page_config(page_title = app_title,
                       page_icon = ":bowling:",
                       layout = "wide")

    st.sidebar.success('Select a page above')

    with st.sidebar:

        with st.expander("❓About"):
            st.markdown("The delta values below each metric express the difference between the  "
                        "all-time average.")

    # --- HEADER ---
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            st.title("Bowling Analytics App")
            st.caption("Bowling seasons: {}".format(season_list))
            st.subheader("Hi there, here you can find your performance over the last two bowling seasons. And compare how you stack up against other players.")
        with right_column:
            st_lottie(animation_bowling_2, height=200, key="coding")

if __name__== "__main__":
    main()

# --- MAP ---
#expands or hides the map of bowling alleys
st.markdown("#")
with st.expander("Click to see the location of bowling alleys"):

    location = df_location.latitude.mean(), df_location.longitude.mean()
    bowling_alleys = folium.Map(location=location,
                                zoom_start=13, tiles="CartoDB Positron")

    ##loop through each bowling alley
    for i,row in df_location.iterrows():

        #set up pop window
        iframe = folium.IFrame('<b>' + str(row['location_name'] + '</b>' +'<br><br>' +str(row['location_address']) +'<br><br>' +'<b> Website</b>: '+ '<br>www.'+str(row['website'])))
        #configure pop window
        popup = folium.Popup(iframe, min_width=220, max_width=200)
        tooltip = "Click to show bowling alley"
        #setting latitude and longitude for each bowling alley
        folium.Marker(location=[row['latitude'], row['longitude']],
                      popup=popup, icon=folium.Icon(color="red", icon_color="white", icon="star", angle=0, prefix="fa"),
                      c=row['location_name'],
                      tooltip=tooltip).add_to(bowling_alleys)

    st_data = st_folium(bowling_alleys, height=550, width=2000)

# --- FILTERS ---
with st.container():
    st.markdown("##")
    st.subheader("Filters")
    st.caption("Please select at least one element in each filter.")

    filter1, filter2 = st.columns(2)
    with filter1:
        player = st.multiselect("Choose a player:", options=df_win_points['nickname'].unique(), default=df_win_points['nickname'].unique())
    with filter2:
        season = st.multiselect("Choose a season:", options=df_win_points['season'].unique(), default=df_win_points['season'].unique())

    df_selection = df_win_points.query(
        "nickname == @player and season == @season")

# --- METRICS ---
with st.container():
    st.subheader('Summary metrics')
    try:
        met1_a, met2_a, met3_a = st.columns(3)
        with met1_a:
            st.metric('total points'.upper(), df_selection['win_points'].sum(),)
        with met2_a:
            st.metric('total games'.upper(), int(len(df_selection['match_id'].unique())))
        with met3_a:
            st.metric('game time (mins)'.upper(), int(round(df_selection['game_time'].sum() / 4, 0)))
        #with met4_a:
        #    st.metric('points per minute'.upper(),
        #              round(df_selection['win_points'].mean() / df_selection['game_time'].mean() * 4, 2))

        met1_b, met2_b, met3_b = st.columns(3)
        with met1_b:
            st.metric('max points'.upper(), df_selection['win_points'].max(),
                      delta=int(df_selection['win_points'].max() - df_win_points['win_points'].max()))
        with met2_b:
            st.metric('average points'.upper(), int(round(df_selection['win_points'].mean(), 0)),
                      delta=int(round(df_selection['win_points'].mean() - df_win_points['win_points'].mean(), 0)))
        with met3_b:
            st.metric('min points'.upper(), df_selection['win_points'].min(),
                      delta = int(df_selection['win_points'].min() - df_win_points['win_points'].min()))
    except:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("#")
        with col2:
            st.markdown("""# 🙅‍♂️ No results 🙅‍♂""")
        with col3:
            st.markdown("#")

# --- CHARTS ---
with st.container():
    st.markdown("###")
    st.markdown("###")
    chart_data = df_selection.groupby(['match_id', 'game_date', 'location_name', 'nickname'])['win_points'].sum()
    test = pd.DataFrame(chart_data.reset_index())

    # wanted result
    bar = alt.Chart(test).mark_bar().encode(
        x=alt.X('match_id:O', title="Match"),
        y=alt.Y('win_points:Q', title="Win points", axis=alt.Axis(labelFontSize=15, titleFontSize=15)),
        color='nickname:N',
        tooltip=[alt.Tooltip('game_date', title="Date"),
                 alt.Tooltip('location_name', title="Location"),
                 alt.Tooltip('match_id', title="Match ID"),
                 alt.Tooltip('nickname', title="Player"),
                 alt.Tooltip('win_points', title="Win points")])
    st.altair_chart(bar, use_container_width=True, theme="streamlit")

