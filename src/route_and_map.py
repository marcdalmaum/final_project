# Libraries
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import itertools
import pandas as pd

def get_G(airports, routes):
    G = nx.from_pandas_edgelist(routes,"source","destination",edge_attr="distance",create_using=nx.DiGraph())
    nx.set_node_attributes(G,airports.continent_code.copy().rename(airports.IATA).to_dict(),'continent_code')
    nx.set_node_attributes(G,airports.latitude.copy().rename(airports.IATA).to_dict(),'latitude')
    nx.set_node_attributes(G,airports.longitude.copy().rename(airports.IATA).to_dict(),'longitude')

    return G

def find_route(G,start_airport,must_go=[],dont_go=[]):

    start = start_airport
    sites = []
    continents = ["NA", "SA", "EU", "AF", "AS", "OC"]

    # Removing from the list of continents the continent of the initial airport
    start_continent = G.nodes[start]['continent_code']
    continents.remove(start_continent)

    # Removing from the list of continents the continents of the "must_go" airports
    for i in range(len(must_go)):
        must_go_continent = G.nodes[must_go[i]]['continent_code']
        if must_go_continent in continents:
            continents.remove(must_go_continent)
    
    while (len(continents)+len(must_go) > 0):
        # Taking only the airports that are in the continents that the route has not yet passed
        pos_airports = [x for x,y in G.nodes(data=True) if (y['continent_code'] in continents)]
        # Adding airports of the "must_go" list
        pos_airports = pos_airports + must_go
        # Deleting airports of the "dont_go" list
        pos_airports = [x for x in pos_airports if x not in dont_go] 
        # Getting the distances to the nearest airports
        pos_dest = nx.single_source_dijkstra(G,start,weight='distance')[0]
        # Removing the first airport (same airport)
        del pos_dest[start]
        # Taking only the airports (and respective distances) that are in the "pos_airports" list
        pos_dest = {key: value for key, value in pos_dest.items() if key in pos_airports}

        if len(pos_dest) > 0:
            x = True
            count = 0
            while x:
                next_route = nx.shortest_path(G,start,list(pos_dest)[count],weight='distance')
                count += 1
                if len(next_route) <= 3:
                    x=False
                    count = 0
                elif len(pos_dest) == count:
                    next_route = nx.shortest_path(G,start,list(pos_dest)[0],weight='distance')
                    x=False
                
            for i in range(len(next_route)):
                if i > 0:
                    sites.append(next_route[i])
                if G.nodes[next_route[i]]['continent_code'] in continents:
                    continents.remove(G.nodes[next_route[i]]['continent_code'])
                if next_route[i] in must_go:
                    must_go.remove(next_route[i])
                start = next_route[i]

    last_route = nx.shortest_path(G,sites[-1],start_airport,weight='distance')
    for i in range(len(last_route)):
        if i > 0:
            sites.append(last_route[i])

    sites = [start_airport]+sites

    return sites

def get_sites_pairs(sites):

    sites_pairs = [(x,y) for x, y in itertools.zip_longest(sites, sites[1:])]
    sites_pairs = sites_pairs[:-1]

    return sites_pairs

def get_total_distance(G, sites_pairs):

    distance = 0
    for pair in sites_pairs:
        d = nx.dijkstra_path_length(G,pair[0],pair[1],weight="distance")
        distance += d

    return distance

def get_map(G, sites, sites_pairs):

    plt.figure(figsize = (30,20))
    m = Basemap(projection='gall')
    m.warpimage(image='bluemarble')
    for s in sites:
        x0, y0 = m(G.nodes[s]['longitude'],G.nodes[s]['latitude'])
        m.scatter(x0,y0,3,marker='o',color='red')
        plt.text(x0,y0+100000,s,fontsize=15,fontweight='bold',ha='center',va='bottom',color="black",bbox=dict(boxstyle="round,pad=0.3", fc="white"))
    for sites_pair in sites_pairs:
        route = nx.dijkstra_path(G,source=sites_pair[0],target=sites_pair[1],weight='Distance')
        ss = [(x,y) for x, y in itertools.zip_longest(route, route[1:])]
        ss = ss[:-1]
        for d_site in ss:
            x, y = m.gcpoints(G.nodes[d_site[0]]['longitude'],G.nodes[d_site[0]]['latitude'],
                            G.nodes[d_site[1]]['longitude'],G.nodes[d_site[1]]['latitude'],500)
            m.plot(x, y,color="#6A6A6A",linewidth=5)
            x2, y2 = m([y['longitude'] for x, y in G.nodes(data=True) if x in d_site],
                    [y['latitude'] for x, y in G.nodes(data=True) if x in d_site])
            m.scatter(x2, y2,color='red',s=50,zorder=2)
    
    return plt.show()

def get_route(airports, sites):

    final_route = {"City": [], "Country": [], "Continent": [], "Airport": [], "IATA": []}
    city = []
    country = []
    continent = []
    airport = []

    for i in range(len(sites)):
        city.append(airports[(airports['IATA'] == sites[i])].values[0][1])
        country.append(airports[(airports['IATA'] == sites[i])].values[0][2])
        continent.append(airports[(airports['IATA'] == sites[i])].values[0][7])
        airport.append(airports[(airports['IATA'] == sites[i])].values[0][0])

    final_route["City"] = city
    final_route["Country"] = country
    final_route["Continent"] = continent
    final_route["Airport"] = airport
    final_route["IATA"] = sites

    return pd.DataFrame.from_dict(final_route)