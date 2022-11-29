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

# STREAMLIT CONFIGURATION

st.set_option('deprecation.showPyplotGlobalUse', False)
st.markdown("<h1 style='text-align: center;'>Ready for a world tour? 🚀</h1>", unsafe_allow_html=True)
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
st.markdown(hide_table_row_index, unsafe_allow_html=True)

header = st.container()
maps = st.container()
distance = st.container()
route = st.container()
flights = st.container()

# STREAMLIT SIDEBAR

form = st.sidebar.form(key='keyword-input')

start_airport_st = form.selectbox("Select your departure airport", options = airports["IATA"].tolist(), 
                                            index=airports["IATA"].tolist().index("BCN"))

must_go_st = form.multiselect("Select some cities you would like to visit", options = airports["IATA"].tolist())

dates_st = form.date_input("Select which day you want to start the adventure", value=None, min_value=dt.datetime.today(), 
                                    max_value=dt.datetime.today() + dt.timedelta(days=365), key=None)

submit = form.form_submit_button('Plan your trip!')

if submit:
    start_airport = str(start_airport_st)
    must_go = must_go_st
    start_date = str(dates_st)

# GET ROUTE AND FLIGHTS

if  start_airport != "" and start_date != "":

    with header:
        st.subheader("Your next trip:")

    G = rm.get_G(airports, routes)
    sites = rm.find_route(G, start_airport, must_go)
    sites_pairs = rm.get_sites_pairs(sites)

    map = rm.get_map(G, sites, sites_pairs)
    with maps:
        st.pyplot(map)

    total_distance = rm.get_total_distance(G, sites_pairs)
    with distance:
        st.text(f"The total distance of your trip is: {total_distance} km")

    final_route = rm.get_route(airports, sites)
    with route:
        st.table(final_route)

    flights_df = pd.DataFrame(columns = ['Departure date', 'Departure airport', 'Departure time', 'Arrival airport', 'Arrival time', 'Airline', 'Flight price'])

    with flights:
            pl = st.empty()

    for i in range(len(sites_pairs)):
        flight_details = fl.get_flight_details(sites_pairs[i][0],sites_pairs[i][1],start_date)

        next_date = (dt.datetime.strptime(start_date,"%Y-%m-%d") + dt.timedelta(days=7)).date()
        start_date = str(next_date)

        flights_df.loc[len(flights_df.index)] = flight_details

        with flights:
            pl.table(flights_df)