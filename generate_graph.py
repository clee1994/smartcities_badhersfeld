import numpy as np 
import pandas as pd

import osmnx as ox
import matplotlib.pyplot as plt

import json
import networkx as nx



def noise_comput(i, frame, graph):

	dist = []
	noise_array = []
	for index, row in frame.iterrows():
		dist.append(np.sqrt((row['lng'] - graph.node[849330149]['x'])**2+(row['lat'] - graph.node[849330149]['y'])**2))
		noise_array.append(row['measurement'])

	dist_order = np.argsort(dist)
	total_dist = np.sum(dist)

	noise_temp = 0
	for i in range(len(dist)):
		noise_temp = noise_temp + (1-dist[i]/total_dist)*noise_array[i]

	return noise_temp


db_file = "data/result2.json"


with open(db_file) as json_data:
	obj = json.load(json_data)
	frame = pd.DataFrame(obj['sensordata'], columns=['lng', 'type','measurement','lat','sensorId','timestamp','SID','eventType'])



place_name = "Bad Hersfeld, Germany"
graph = ox.graph_from_place(place_name)


for i in graph.node:
	graph.node[i]['noise'] = noise_comput(i, frame, graph)

for i in graph.edges:
	graph[i[0]][i[1]][i[2]]['noise_cc'] = 0.5*(graph.node[i[0]]['noise']+graph.node[i[1]]['noise'])
	graph[i[0]][i[1]][i[2]]['noise_cc_len'] = graph[i[0]][i[1]][i[2]]['length'] * graph[i[0]][i[1]][i[2]]['noise_cc']

graph[2153111550][2153108850][0]['teessst'] = 124
graph[2153111550][2153108850][0]


#noise_comput(849330149, frame, graph)



#nx.shortest_path(graph,source=267198459,target=1034289119,weight='length')



#nodes, edges = ox.graph_to_gdfs(graph)   

#fig, ax = plt.subplots()  
#edges.plot(ax=ax, linewidth=1, edgecolor='#BC8F8F')  



nx.write_gpickle(graph, "graphs/data_source_graph") 
#visualization
#fig, ax = ox.plot_graph(graph)

#import matplotlib.pyplot as plt

#plt.plot(frame['lng'], frame['lat'] , "o")

