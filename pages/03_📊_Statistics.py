# --- LIBRARIES ---
import requests
import pandas as pd
import altair as alt

import streamlit as st
from streamlit_lottie import st_lottie
#from streamlit_extras import extra

# TODO:
#  1) add first throw pin fall statistic

# --- CONNECTING AND LOADING DATA ---
url = "https://raw.githubusercontent.com/P33Rview/Bowling_league_app/master/datasets/SPARE_STRIKE.csv"
dataframe_win_points = pd.read_csv(url)

# DATAFRAMES
df_win_points = pd.DataFrame(dataframe_win_points)

# --- STORING ASSETS ---
def load_animation(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

animation_bowling_1 = load_animation("https://assets10.lottiefiles.com/datafiles/qbAoVVjPqpGHkwP/data.json")
animation_bowling_2 = load_animation("https://assets10.lottiefiles.com/private_files/lf30_rivr2ir4.json")
animation_bowling_3 = load_animation("https://assets6.lottiefiles.com/packages/lf20_evpfhziw.json")

#subheaders showing the season list
seasons = df_win_points.season.unique()
season_list = (', '.join(seasons))

def main():

    st.set_page_config(page_title = "Statistics",
                       page_icon = ":bar_chart:",
                       layout = "wide")

    with st.sidebar:
        with st.expander("❓About"):
            st.markdown("The delta values below each metric express the difference between the  "
                        "all-time average.")

    # --- HEADER ---
    with st.container():
        st.title("Statistics")
        st.caption("Bowling seasons: {}".format(season_list))
        st.subheader("In this section, you can view the basic bowling statistics, along with strike and spare percentage.")
        st.markdown("""
            <style>
            .big-font {
                font-size:25px !important;
            }
            .medium-font {
                font-size:15px;
            }
            </style>
            """, unsafe_allow_html=True)
        with st.expander("Click to view explanation of statistics"):

            text, text1, text2 = st.columns(3)
            with text:
                st.markdown("##")
                st.markdown("##")
                st_lottie(animation_bowling_3, key='coding')

            with text1:
                st.markdown('<p class="big-font">Basic statistics explained: </p>', unsafe_allow_html=True)
                st.markdown(
                    """**<p class="big-font"><span style='color:cadetblue'>Strike</span>**</p> A strike is when you knock all the pins on the first throw in a frame.""",
                    unsafe_allow_html=True)
                st.markdown(
                    """**<p class="big-font"><span style='color:black'>Strike percentage</span>**</p> Expresses how often a player has a strike.""",
                    unsafe_allow_html=True)
                st.markdown(
                    """**<p class="big-font"><span style='color:gray'>Split</span></p>** A split is when the headpin gets knocked down and there is a space  
                     of at least one pin between two of the pins in the back row.""",
                    unsafe_allow_html=True)
            with text2:
                st.markdown("""<p class="big-font"><span style='color:white'>a</span></p>""", unsafe_allow_html=True)
                st.markdown(
                    """**<p class="big-font"><span style='color:cadetblue'>Spare</span>**</p> A spare is when you knock all the pins in two shots in a frame.""",
                    unsafe_allow_html=True)
                st.markdown(
                    """**<p class="big-font"><span style='color:black'>Spare percentage</span>**</p> Expresses how often a player has a spare.""",
                    unsafe_allow_html=True)
                st.markdown(
                    """**<p class="big-font"><span style='color:gray'>First throw gutter</span></p>** A first throw gutter occurs when the player does not knock down   
                    a single pin in his first throw.""",
                    unsafe_allow_html=True)

if __name__== "__main__":
    main()

# --- FILTERS ---
with st.container():
    st.markdown("##")
    st.subheader("Filter")
    st.caption("Please select at least one element in the filter.")

    season = st.multiselect("Choose a season:", options=df_win_points['season'].unique(),
                            default='2024/2025')
    #filter1, filter2 = st.columns(2)
    #with filter1:
    #    season = st.multiselect("Choose a season:", options=df_win_points['season'].unique(),
    #                            default=df_win_points['season'].unique())
    #with filter2:
    #    st.markdown("#")
    #    location_name = st.multiselect("Choose a bowling alley:", options=df_win_points['location_name'].unique(),
    #                                   default=df_win_points['location_name'].unique())

# query used for filtering
df_selection = df_win_points.query(
        "season == @season")

# --- CHARTS ---
with st.container():
    st.markdown("###")

    #strike and spare percentage metrics
    adv_text1, adv_text2, adv_text3, adv_text4 = st.columns(4)

    with adv_text1:
        st.subheader("Pichy")
        st.metric("Strike percentage", value=str(
            round(df_selection['strike_percentage'].loc[df_selection['nickname'] == 'Pichy'].mean() * 100, 1)) + " %",
                  delta=str(round(df_selection['strike_percentage'].loc[df_selection['nickname'] == 'Pichy'].mean() * 100 -
                      df_win_points['strike_percentage'].mean() * 100, 1)) + " %")

        st.metric("Spare percentage", value=str(
            round(df_selection['spare_percentage'].loc[df_selection['nickname'] == 'Pichy'].mean() * 100, 1)) + " %",
                  delta=str(round(df_selection['spare_percentage'].loc[df_selection['nickname'] == 'Pichy'].mean() * 100 -
                      df_win_points['spare_percentage'].mean() * 100, 1)) + " %")

        st.markdown("#")

    with adv_text2:
        st.subheader("Helcl")
        st.metric("Strike percentage", value=str(
            round(df_selection['strike_percentage'].loc[df_selection['nickname'] == 'Helcl'].mean() * 100, 1)) + " %",
                  delta=str(
                      round(df_selection['strike_percentage'].loc[df_selection['nickname'] == 'Helcl'].mean() * 100 -
                            df_win_points['strike_percentage'].mean() * 100, 1)) + " %")

        st.metric("Spare percentage", value=str(
            round(df_selection['spare_percentage'].loc[df_selection['nickname'] == 'Helcl'].mean() * 100, 1)) + " %",
                  delta=str(
                      round(df_selection['spare_percentage'].loc[df_selection['nickname'] == 'Helcl'].mean() * 100 -
                            df_win_points['spare_percentage'].mean() * 100, 1)) + " %")

        st.markdown("#")

    with adv_text3:
        st.subheader("Vrbic")
        st.metric("Strike percentage", value=str(
            round(df_selection['strike_percentage'].loc[df_selection['nickname'] == 'Vrbic'].mean() * 100, 1)) + " %",
                  delta=str(
                      round(df_selection['strike_percentage'].loc[df_selection['nickname'] == 'Vrbic'].mean() * 100 -
                            df_win_points['strike_percentage'].mean() * 100, 1)) + " %")

        st.metric("Spare percentage", value=str(
            round(df_selection['spare_percentage'].loc[df_selection['nickname'] == 'Vrbic'].mean() * 100, 1)) + " %",
                  delta=str(
                      round(df_selection['spare_percentage'].loc[df_selection['nickname'] == 'Vrbic'].mean() * 100 -
                            df_win_points['spare_percentage'].mean() * 100, 1)) + " %")

        st.markdown("#")

    with adv_text4:
        st.subheader("Spinda")
        st.metric("Strike percentage", value=str(
            round(df_selection['strike_percentage'].loc[df_selection['nickname'] == 'Spinda'].mean() * 100, 1)) + " %",
                  delta=str(
                      round(df_selection['strike_percentage'].loc[df_selection['nickname'] == 'Spinda'].mean() * 100 -
                            df_win_points['strike_percentage'].mean() * 100, 1)) + " %")

        st.metric("Spare percentage", value=str(
            round(df_selection['spare_percentage'].loc[df_selection['nickname'] == 'Spinda'].mean() * 100, 1)) + " %",
                  delta=str(
                      round(df_selection['spare_percentage'].loc[df_selection['nickname'] == 'Spinda'].mean() * 100 -
                            df_win_points['spare_percentage'].mean() * 100, 1)) + " %")

        st.markdown("#")
        st.markdown('''
               <style>

               [data-testid="metric-container"] {
                   width: auto;
                   justify-content: center;
                   margin: auto;
                   background-color: #f1f2f6;
                   border-radius: 10px;
                   padding: 12%   
               }

               [data-testid="metric-container"] > div {
                   width: fit-content;
                   justify-content: center;
                   margin: auto;
                   background-color: #f1f2f6;
                   border-radius: 10px;

               }

               [data-testid="metric-container"] label {
                   width: fit-content;
                   margin: auto;
               }

               </style>
               ''', unsafe_allow_html=True)
    # upper section bar charts
    col1_upper, col2_upper = st.columns(2)

    with col1_upper:
        st.subheader('Strikes')

        # initializing the underlying data
        chart_data_strike = df_selection.groupby(['nickname'])[['strike_count']].sum()
        data_ready_strike = pd.DataFrame(chart_data_strike.reset_index())

        # first layer of the chart - bar chart
        bar_strike = alt.Chart(data_ready_strike).mark_bar(
            cornerRadiusTopRight=5,
            cornerRadiusBottomRight=5,
            color='salmon',
            size=35
        ).encode(
            x=alt.X('strike_count:Q', title=None,
                    axis=alt.Axis(grid=False, labels=False)),
            y=alt.Y('nickname:O', title=None,
                    sort=alt.EncodingSortField(field='strike_count', op='sum', order='descending'),
                    axis=alt.Axis(labelFontSize=15, titleFontSize=15, grid=False)),
            text='strike_count:Q',
            tooltip=[alt.Tooltip('nickname', title='Nickname'),
                     alt.Tooltip('strike_count', title='Total strikes')]).properties(height=200, width=600)

        combined_strike = bar_strike + bar_strike.mark_text(align="left", dx=10, font='sans-serif', fontSize=15)
        st.altair_chart(combined_strike, use_container_width=True, theme="streamlit")

    with col2_upper:
        st.subheader('Spares')

        # initializing the underlying data
        chart_data_spare = df_selection.groupby(['nickname'])[['spare_count']].sum()
        data_ready_spare = pd.DataFrame(chart_data_spare.reset_index())

        # first layer of the chart - bar chart
        bar_spare = alt.Chart(data_ready_spare).mark_bar(
            cornerRadiusTopRight=5,
            cornerRadiusBottomRight=5,
            color='bisque',
            size=35
        ).encode(
            x=alt.X('spare_count:Q', title=None,
                    axis=alt.Axis(grid=False, labels=False)),
            y=alt.Y('nickname:O', title=None,
                    sort=alt.EncodingSortField(field='spare_count', op='sum', order='descending'),
                    axis=alt.Axis(labelFontSize=15, titleFontSize=15, grid=False)),
            text='spare_count:Q',
            tooltip=[alt.Tooltip('nickname', title='Nickname'),
                     alt.Tooltip('spare_count', title='Total spares')]).properties(height=200, width=600)

        # second layer of the chart - text label overlay
        combined_spare = bar_spare + bar_spare.mark_text(align="left", dx=10, font='sans-serif', fontSize=15)
        st.altair_chart(combined_spare, use_container_width=True, theme="streamlit")

    #bottom section bar charts
    col1_lower, col2_lower = st.columns(2)

    with col1_lower:
        st.subheader('Splits')
        # initializing the underlying data
        chart_data_split = df_selection.groupby(['nickname'])[['split_count']].sum()
        data_ready_split = pd.DataFrame(chart_data_split.reset_index())
        # first layer of the chart - bar chart
        bar_split = alt.Chart(data_ready_split).mark_bar(
            cornerRadiusTopRight=5,
            cornerRadiusBottomRight=5,
            color='slategray',
            size=35
        ).encode(
            x=alt.X('split_count:Q', title=None,
                    axis=alt.Axis(grid=False, labels=False)),
            y=alt.Y('nickname:O', title=None,
                    sort=alt.EncodingSortField(field='split_count', op='sum', order='descending'),
                    axis=alt.Axis(labelFontSize=15, titleFontSize=15, grid=False)),
            text='split_count:Q',
            tooltip=[alt.Tooltip('nickname', title='Nickname'),
                     alt.Tooltip('split_count', title='Total splits')]).properties(height=200, width=600)
        # second layer of the chart - text label overlay
        combined_split = bar_split + bar_split.mark_text(align="left", dx=10, font='sans-serif', fontSize=15)
        st.altair_chart(combined_split, use_container_width=True, theme="streamlit")

    with col2_lower:
        st.subheader('First gutters')

        # initializing the underlying data
        chart_data_gutter_1 = df_selection.groupby(['nickname'])[['gutter_1_count']].sum()
        data_ready_gutter_1 = pd.DataFrame(chart_data_gutter_1.reset_index())

        # first layer of the chart - bar chart
        bar_gutter_1 = alt.Chart(data_ready_gutter_1).mark_bar(
            cornerRadiusTopRight=5,
            cornerRadiusBottomRight=5,
            color='lightsteelblue',
            size=35
        ).encode(
            x=alt.X('gutter_1_count:Q', title=None,
                    axis=alt.Axis(grid=False, labels=False)),
            y=alt.Y('nickname:O', title=None,
                    sort=alt.EncodingSortField(field='gutter_1_count', op='sum', order='descending'),
                    axis=alt.Axis(labelFontSize=15, titleFontSize=15, grid=False)),
            text='gutter_1_count:Q',
            tooltip=[alt.Tooltip('nickname', title='Nickname'),
                     alt.Tooltip('gutter_1_count', title='Total first gutters')]).properties(height=200, width=600)

        # second layer of the chart - text label overlay
        combined_gutter_1 = bar_gutter_1 + bar_gutter_1.mark_text(align="left", dx=10, font='sans-serif', fontSize=15)
        st.altair_chart(combined_gutter_1, use_container_width=True, theme="streamlit")


    # CSS command to hide the view fullscreen widget
    st.markdown(
        """
    <style>
    button[title="View fullscreen"] {
        display: none;
    }
    </style>
    """,
        unsafe_allow_html=True)
