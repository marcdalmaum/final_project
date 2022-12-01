# WORLD TOUR PLANNER PROJECT

## OBJECTIVE

The main object of this project is to create an app to find the optimal route to travel around the world, passing through the 6 continents, given the following data:

- Departure airport
- Cities to visit
- Start date 

## ACQUISITION

Two databases have been obtained with all airports in the world and all possible routes from [Openflights.org](https://openflights.org/).

## CLEANING

In order to clean the dataframe, some functions have been used, saved in the [clean_dataframes.py](src/clean_dataframes.py) document.

## ROUTE AND MAP

Once the databases have been cleaned, a network graph has been created in order to be able to calculate the optimal route and plot it on a map, the functions can be found in the [route_and_map.py](src/route_and_map.py) document.

## SCRAPE FLIGHTS

Once the route has been created, the best flights have been scraped according to the selected dates, on [Kayak.es](https://www.kayak.es/). The code can be found in the [flights.py](src/flights.py) document.

## SHOW RESULTS

Finally, a streamlit app has been created to show the results of the queries:

<img src="images/streamlit.gif">