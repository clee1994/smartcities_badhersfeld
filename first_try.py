import numpy as np 
import pandas as pd


#testing geoplotlib
import geoplotlib


data = pd.read_csv('data/bus.csv')
geoplotlib.dot(data)
geoplotlib.show()