import numpy as np 
import pandas as pd

import osmnx as ox
import matplotlib.pyplot as plt

import json
import networkx as nx

import random

from tqdm import tqdm


from scipy import spatial





def noise_comput(i, frame, graph):

	dist = []
	noise_array = []
	for index, row in frame.iterrows():
		dist.append(np.sqrt((row['lng'] - graph.node[i]['x'])**2+(row['lat'] - graph.node[i]['y'])**2))
		noise_array.append(row['measurement'])

	dist_order = np.argsort(dist)
	total_dist = np.sum(dist)

	noise_temp = 0
	weigth_no = []
	for i in range(len(dist)):
		weigth_no.append( (1-(dist[i]/total_dist)))

	noise_temp = 0
	for i in range(len(dist)):
		noise_temp = noise_temp + (weigth_no[i]/np.sum(weigth_no)) *noise_array[i]

	#import pdb; pdb.set_trace()

	return noise_temp


# def dist_comput(i,graph):
# 	dist = []
# 	noise_array = []
# 	for index, row in frame.iterrows():
# 		dist.append(np.sqrt((row['lng'] - graph.node[i]['x'])**2+(row['lat'] - graph.node[i]['y'])**2))
# 		noise_array.append(row['measurement'])

# 	dist_order = np.argsort(dist)
# 	total_dist = np.sum(dist)


db_file = "data/result2.json"



with open(db_file) as json_data:
	obj = json.load(json_data)
	frame = pd.DataFrame(obj['sensordata'], columns=['lng', 'type','measurement','lat','sensorId','timestamp','SID','eventType'])


#new small df
df_frame_proc = pd.DataFrame()
for i in np.unique(frame['sensorId']):
	temp_data = {'lng':[list(frame['lng'][frame['sensorId']==str(i)])[0]],
				'type':[list(frame['type'][frame['sensorId']==str(i)])[0]],
				'measurement': [np.nanmean(frame['measurement'][frame['sensorId']==str(i)])],
				'lat': [list(frame['lat'][frame['sensorId']==str(i)])[0]], 
				'sensorId' :[list(frame['sensorId'][frame['sensorId']==str(i)])[0]],
				'timestamp' : [list(frame['timestamp'][frame['sensorId']==str(i)])[0]], 
				'SID' : [list(frame['SID'][frame['sensorId']==str(i)])[0]],
 				'eventType': [list(frame['eventType'][frame['sensorId']==str(i)])[0]]}


	df_temp = pd.DataFrame(temp_data)


	df_frame_proc= df_frame_proc.append(df_temp)


frame = df_frame_proc

place_name = "Bad Hersfeld, Germany"
#place_name = "Krombach, Germany"
graph = ox.graph_from_place(place_name)


#define those
max_y = 50.885
max_x = 9.775
min_y = 50.842
min_x = 9.650

#shrink graph
membersProcessed = 0
rem_member = []
for i in graph.node:
	if (graph.node[i]['x'] > min_x) and (graph.node[i]['x'] < max_x) and (graph.node[i]['y'] > min_y) and (graph.node[i]['y'] < max_y):
		graph.node[i]['noise'] = noise_comput(i, frame, graph)
	else:
		rem_member.append(i)
	membersProcessed += 1
	print('Progress: {}/{} members processed'.format(membersProcessed, len(graph.node)))

for i in rem_member:
	graph.remove_node(i)

membersProcessed = 0
for i in graph.edges:
	graph[i[0]][i[1]][i[2]]['noise_cc'] = 0.5*(graph.node[i[0]]['noise']+graph.node[i[1]]['noise'])
	graph[i[0]][i[1]][i[2]]['noise_cc_len'] = graph[i[0]][i[1]][i[2]]['length'] * graph[i[0]][i[1]][i[2]]['noise_cc']
	membersProcessed += 1
	print('Progress: {}/{} members processed'.format(membersProcessed, len(graph.edges)))

nodes, edges = ox.graph_to_gdfs(graph)   
bucket1 = np.percentile(edges['noise_cc'],0.333)
bucket2 = np.percentile(edges['noise_cc'],0.666)

membersProcessed = 0
for i in graph.edges:
	if graph[i[0]][i[1]][i[2]]['noise_cc'] < bucket1:
		graph[i[0]][i[1]][i[2]]['color'] = 'green'
	elif (graph[i[0]][i[1]][i[2]]['noise_cc'] >= bucket1) and (graph[i[0]][i[1]][i[2]]['noise_cc'] < bucket2):
		graph[i[0]][i[1]][i[2]]['color'] = 'yellow'
	else:
		graph[i[0]][i[1]][i[2]]['color'] = 'red'
	membersProcessed += 1
	print('Progress: {}/{} members processed'.format(membersProcessed, len(graph.edges)))



#colors = ['red','black','green','blue','orange','yellow']
#for i in graph.edges:
#	graph[i[0]][i[1]][i[2]]['noise_cc'] = 10
#	graph[i[0]][i[1]][i[2]]['noise_cc_len'] = 10
	#graph[i[0]][i[1]][i[2]]['color'] = random.choice(colors) #color based on rule


#graph[2153111550][2153108850][0]['teessst'] = 124
#graph[2153111550][2153108850][0]

nodes, edges = ox.graph_to_gdfs(graph) 
edges_red = edges[edges['color']=='red']
edges_yellow = edges[edges['color']=='yellow']
edges_green = edges[edges['color']=='green']

#noise_comput(849330149, frame, graph)

#nodes, edges = ox.graph_to_gdfs(graph)   

fig, ax = plt.subplots()
edges_red.plot(ax=ax, linewidth=1, edgecolor='red')
edges_yellow.plot(ax=ax, linewidth=1, edgecolor='yellow')
edges_green.plot(ax=ax, linewidth=1, edgecolor='green')

plt.show()
fig.savefig('./figures/super_map.png')



# from scipy import spatial

# A = np.array(nodes[['x','y']])

# distance,index_s = spatial.KDTree(A).query([9.6757233,50.8612437])

# distance,index_e = spatial.KDTree(A).query([9.6631338,50.8575636])



# #edgecolor='#BC8F8F'


# #category

# #for i in range(300):
# #edges[0:10]



# #find closest nodes




# nx.shortest_path(graph,source=267198459,target=1034289119,weight='noise_cc_len')



# np.array()



#fig, ax = plt.subplots()  
#edges.plot(ax=ax, linewidth=1, edgecolor='#BC8F8F')  



nx.write_gpickle(graph, "graphs/data_source_graph") 
#visualization
#fig, ax = ox.plot_graph(graph)

#import matplotlib.pyplot as plt

#plt.plot(frame['lng'], frame['lat'] , "o")

