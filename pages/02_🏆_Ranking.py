# --- LIBRARIES ---
import pandas as pd
import altair as alt

import streamlit as st
from annotated_text import annotated_text


# --- CONNECTING AND LOADING DATA ---
url = "https://raw.githubusercontent.com/P33Rview/Bowling_league_app/master/datasets/RANKING.csv"
dataframe_ranking = pd.read_csv(url)

# DATAFRAMES
df_win_points = pd.DataFrame(dataframe_ranking)

#subheaders showing the season list
seasons = df_win_points.season.unique()
season_list = (', '.join(seasons))

def main():
    st.set_page_config(page_title = "Ranking",
                       page_icon = ":trophy:",
                       layout = "wide")

    # --- HEADER ---
    with st.container():
        st.title("Ranking")
        st.caption("Bowling seasons: {}".format(season_list))
        st.subheader("Here you can track your total season ranking either by game points or by total placement.")

    season_1, season_2, season_3 = st.columns(3)
    with season_1:
        st.markdown("")
        annotated_text(("Season 2021/2022 Ranking", "", "#F0F2F6"))
        st.write("""🥇 Helcl    
                 🥈 Spinda    
                 🥉 Pichy""")

    with season_2:
        st.markdown("")
        annotated_text(("Season 2022/2023 Ranking", "", "#F0F2F6"))
        st.write("""🥇 Helcl    
                    🥈 Vrbic    
                    🥉 Spinda""")

    with season_3:
        st.markdown("")
        annotated_text(("Season 2023/2024 Ranking", "", "#F0F2F6"))
        st.write("""🥇 ?    
                    🥈 ?    
                    🥉 ?""")
if __name__== "__main__":
    main()

# --- FILTERS ---
with st.container():
    st.markdown("##")
    st.subheader("Filter")
    st.caption("Please select at least one element in the filter.")
    season = st.multiselect("Choose a season:", options=df_win_points['season'].unique(),
                            default='2023/2024')
    # filter1, filter2 = st.columns(2)
    # with filter1:
    #    season = st.multiselect("Choose a season:", options=df_win_points['season'].unique(),
    #                            default=df_win_points['season'].unique())
    # with filter2:
    #    st.markdown("#")
    #    location_name = st.multiselect("Choose a bowling alley:", options=df_win_points['location_name'].unique(),
    #                                   default=df_win_points['location_name'].unique())

# query used for filtering
df_selection = df_win_points.query("season == @season")

# --- CHARTS ---
with st.container():
    col1, col2 =st.columns(2)

    with col1:
        st.subheader('Total points')

        # initializing the underlying data
        chart_win_points = df_selection.groupby(['nickname'])[['win_points']].sum()
        data_ready_win_points  = pd.DataFrame(chart_win_points.reset_index())

        # first layer of the chart - bar chart
        bar_win_points = alt.Chart(data_ready_win_points).mark_bar(
            cornerRadiusTopRight=5,
            cornerRadiusBottomRight=5,
            color='cadetblue',
            size=35
        ).encode(
            x=alt.X('win_points:Q', title=None,
                    axis=alt.Axis(grid=False, labels=False)),
            y=alt.Y('nickname:O', title=None,
                    sort=alt.EncodingSortField(field='win_points', op='sum', order='descending'),
                    axis=alt.Axis(labelFontSize=15, titleFontSize=15, grid=False)),
            text='win_points:Q',
            tooltip=[alt.Tooltip('nickname', title='Nickname'),
                     alt.Tooltip('win_points', title='Total points')]).properties(height=200, width=600)
        # second layer of the chart - text label overlay
        combined_win_points = bar_win_points + bar_win_points.mark_text(align="left", dx=10, font='sans-serif', fontSize=15)
        st.altair_chart(combined_win_points, use_container_width=True, theme="streamlit")

    with col2:
        st.subheader('Total placement')

        # initializing the underlying data
        chart_placement = df_selection.groupby(['nickname'])[['placement']].mean().round(2)
        data_placement = pd.DataFrame(chart_placement.reset_index())

        # first layer of the chart - bar chart
        bar_placement = alt.Chart(data_placement).mark_bar(
            cornerRadiusTopRight=5,
            cornerRadiusBottomRight=5,
            color='papayawhip',
            size=35
        ).encode(
            x=alt.X('placement:Q', title=None,
                    axis=alt.Axis(grid=False, labels=False)),
            y=alt.Y('nickname:O', title=None,
                    sort=alt.EncodingSortField(field='placement', op='sum', order='ascending'),
                    axis=alt.Axis(labelFontSize=15, titleFontSize=15, grid=False)),
            text='placement:Q',
            tooltip=[alt.Tooltip('nickname', title='Nickname'),
                     alt.Tooltip('placement', title='Total placement')]).properties(height=200, width=600)
        # second layer of the chart - text label overlay
        combined_placement = bar_placement + bar_placement.mark_text(align="left", dx=10, font='sans-serif', fontSize=15)
        st.altair_chart(combined_placement, use_container_width=True, theme="streamlit")

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
