# Libraries
import streamlit as st
import pandas as pd
from src import route_and_map as rm
from src import flights as fl
import datetime as dt

start_airport = ""
must_go = []
start_date = ""

airports = pd.read_csv("data/airports_cleaned.csv", keep_default_na=False)
routes = pd.read_csv("data/routes_cleaned.csv", keep_default_na=False)

# ------------------------------------- STREAMLIT CONFIGURATION -------------------------------------

st.set_page_config(layout="wide") 
st.set_option('deprecation.showPyplotGlobalUse', False)
title = st.empty()
title.markdown("<h1 style='text-align: center;'>Ready for a world tour? 🚀</h1>", unsafe_allow_html=True)

giphy = st.empty()
with giphy:
    col1, col2, col3 = st.columns([0.9,2,0.9])
    with col1:
        st.write("")
    with col2:
        st.markdown("![Alt Text](https://media4.giphy.com/media/PhGhQF98OhZUYLPhaM/giphy.gif?cid=ecf05e47ba4sk4ndcur9zmj3dfk3ygacoqv9dl1nyob5hpqf&rid=giphy.gif&ct=g)")
    with col3:
        st.write("")

hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
st.markdown(hide_table_row_index, unsafe_allow_html=True)

maps = st.container()
route = st.container()
distance = st.container()
flights = st.container()

# ---------------------------------------- STREAMLIT SIDEBAR ----------------------------------------

form = st.sidebar.form(key='keyword-input')

start_airport_st = form.selectbox("Select your departure airport:", options = airports["airport"].tolist(), 
                                            index=airports["airport"].tolist().index("Barcelona (BCN)"))

must_go_st = form.multiselect("Select some cities you would like to visit:", options = airports["airport"].tolist())

dates_st = form.date_input("Select which day you want to start the adventure:", value=None, min_value=dt.datetime.today(), 
                                    max_value=dt.datetime.today() + dt.timedelta(days=365), key=None)

submit = form.form_submit_button('Plan your trip!')

if submit:

    title.empty()
    giphy.empty()

    start_airport = airports.loc[airports["airport"] == str(start_airport_st), "IATA"].iloc[0]

    must_go = []
    for i in must_go_st:
        must_go.append(airports.loc[airports["airport"] == i, "IATA"].iloc[0])

    start_date = str(dates_st)

# -------------------------------------- GET ROUTE AND FLIGHTS --------------------------------------

if  start_airport != "" and start_date != "":

    G = rm.get_G(airports, routes)
    sites = rm.find_route(G, start_airport, must_go)
    sites_pairs = rm.get_sites_pairs(sites)

    map = rm.get_map(G, sites, sites_pairs)
    with maps:
        st.subheader("Mapping your next trip:")
        st.pyplot(map)

    final_route = rm.get_route(airports, sites)
    with route:
        st.subheader("Route details:")
        st.table(final_route)

    total_distance = round(rm.get_total_distance(G, sites_pairs), 2)
    with distance:
        st.text(f"The total distance of your trip is: {total_distance} km")

    flights_df = pd.DataFrame(columns = ['Departure date', 'Departure airport', 'Departure time', 'Arrival airport', 'Arrival time', 'Airline', 'Flight price'])

    with flights:
        st.subheader("Flight details:")
        pl = st.empty()

    for i in range(len(sites_pairs)):
        flight_details = fl.get_flight_details(sites_pairs[i][0],sites_pairs[i][1],start_date)

        next_date = (dt.datetime.strptime(start_date,"%Y-%m-%d") + dt.timedelta(days=7)).date()
        start_date = str(next_date)

        flights_df.loc[len(flights_df.index)] = flight_details

        with flights:
            pl.table(flights_df)