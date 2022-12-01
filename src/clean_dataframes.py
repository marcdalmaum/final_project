# LIBRARIES
import pandas as pd
import pycountry_convert as pc
import numpy as np
import geopy.distance

# ---------------------------------------- AIRPORTS DATABASE ----------------------------------------

# Importing the CSV document with all the airports
def get_airports_df():
    airports_df = pd.read_csv("../data/airports.csv", header=None)
    airports_df.columns = ["airport_id", "airport_name", "city", "country", "IATA", "ICAO", "latitude", "longitude", 
                        "altitude", "time_zone", "dst", "tz_database_time_zone", "type", "source"]
    airports_df.drop(["airport_id", "ICAO", "altitude", "time_zone", "dst", "tz_database_time_zone", "type", "source"], axis = 1, inplace = True)
    return airports_df

airports_df = get_airports_df()

# Getting the country code with the pycountry_convert library
def get_continent_code():
    country_codes = []
    for _, row in airports_df.iterrows():
        try:
            country_code = pc.country_name_to_country_alpha2(row.country, cn_name_format="default")
            continent_code = pc.country_alpha2_to_continent_code(country_code)
            country_codes.append(continent_code)
        except:
            country_codes.append(np.nan)
    return country_codes

airports_df["continent_code"] = get_continent_code()

# Dropping null values
def drop_null_values():
    for column in airports_df:
        airports_df[column] = airports_df[column].replace([r"\N"],np.nan)
    airports_df.dropna(how="any", inplace=True)

drop_null_values()

# Adding the names of the continents
def get_continents():
    continents = {"AS":"Asia", "AF":"Africa", "NA":"North America","SA":"South America", "EU":"Europe", "OC":"Oceania"}
    airports_df['continent'] = airports_df['continent_code'].map(continents)

get_continents()

# Creating a new column with the city and the IATA code
def get_airports():
    airports_df["airport"] = airports_df["city"] +" ("+ airports_df["IATA"] +")"

get_airports()


# ----------------------------------------- ROUTES DATABASE -----------------------------------------

# Importing the CSV document with all the possible routes
def get_routes_df():
    routes = pd.read_csv("../data/routes.csv", header=None)
    routes.columns = ["airline", "airline_id", "source", "source_airport_id", "destination", 
                        "destination_airport_id", "codeshare", "stops", "equipment"]
    routes.drop(["airline", "airline_id", "source_airport_id", "destination_airport_id", "codeshare", "stops", "equipment"], axis = 1, inplace = True)
    routes.drop_duplicates(subset=["source", "destination"], inplace=True)
    return routes

routes = get_routes_df()

# Merging dataframes to obtain information about the airport of departure and arrival
def merge_dataframes():
    routes_source = pd.merge(left=routes, right=airports_df[["IATA","latitude","longitude","continent_code"]], left_on="source", right_on="IATA")
    routes_source.drop(["IATA"], axis = 1, inplace = True)
    routes_source.rename(columns={"latitude":"source_lat", "longitude":"source_lon", "continent_code":"source_code"}, inplace=True)

    routes_df = pd.merge(left=routes_source, right=airports_df[["IATA","latitude","longitude","continent_code"]], left_on="destination", right_on="IATA")
    routes_df.drop(["IATA"], axis = 1, inplace = True)
    routes_df.rename(columns={"latitude":"dest_lat", "longitude":"dest_lon", "continent_code":"dest_code"}, inplace=True)
    
    return routes_df

routes_df = merge_dataframes()

# Calculating the distance between airports
def get_distance():  
    distance = []
    for i in range(len(routes_df)):
        source = (routes_df.source_lat[i], routes_df.source_lon[i])
        dest = (routes_df.dest_lat[i], routes_df.dest_lon[i])
        distance.append(geopy.distance.distance(source, dest).km)
    return np.round(distance, 2)

routes_df["distance"] = get_distance()

# Eliminating airports where no trade route exists
airports_df = airports_df[airports_df.IATA.isin(list(routes_df.source) + list(routes_df.destination))]

# Saving both dataframes into CSV files
airports_df.to_csv('../data/airports_cleaned.csv', index=False)
routes_df.to_csv('../data/routes_cleaned.csv', index=False)