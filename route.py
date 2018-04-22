import numpy as np 
import pandas as pd

import osmnx as ox
import matplotlib.pyplot as plt

import json
import networkx as nx

import random

from tqdm import tqdm


from scipy import spatial

import uuid


orig_xy = [9.6757233,50.8612437]
target_xy = [9.6631338,50.8575636]

create_route(orig_xy,target_xy)

def create_route(orig_xy, target_xy):
	unique_filename = str(uuid.uuid4())


	#plt.ioff()

	graph = nx.read_gpickle("graphs/data_source_graph")
	nodes, edges = ox.graph_to_gdfs(graph,nodes=True,edges=True)  


	osmids = np.array(graph.nodes)
	A = np.array([])
	for i in osmids:
		A = np.append(A,[graph.nodes[i]['x'],graph.nodes[i]['y']])
	A = A.reshape((int(len(A)/2),2))

	#A = np.array(nodes[['x','y']])

	#osmid = np.array(nodes['osmid'])

	distance,index_s = spatial.KDTree(A).query(orig_xy)
	orig_node = osmids[index_s]

	distance,index_e = spatial.KDTree(A).query(target_xy)
	target_node = osmids[index_e]



	#orig_xy = (9.6757233,50.8612437)
	#target_xy = (9.6631338,50.8575636)
	#orig_node = ox.get_nearest_node(graph, orig_xy, method='euclidean')
	#target_node = ox.get_nearest_node(graph, target_xy, method='euclidean')



	route = nx.shortest_path(graph,source=orig_node,target=target_node,weight='length')


	#orig_xy(orig_point.y, orig_point.x)

	fig, ax = ox.plot_graph_route(graph, route, origin_point=orig_xy, destination_point=target_xy,show=False)
	fig.savefig('./figures/'+unique_filename+".png")


	return './figures/'+unique_filename+".png"
#plt.show()

street_name = "Am Markt 10, Bad Hersfeld"

def string_to_xy(name_bla):

	req_string ='https://maps.googleapis.com/maps/api/geocode/json?address='+name_bla.replace(" ","+")

	import requests

	response = requests.get(req_string)

	resp_json_payload = response.json()

	resss = resp_json_payload['results'][0]['geometry']['location']
	return [resss['lng'],resss['lat']]


