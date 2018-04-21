import pandas as pd

path = 'C:\Users\demreis3\Documents\smartcities_badhersfeld\data\BDHData\0ab9938e-0aa9-49cd-b9b5-68b77e6a97eb.txt'
data = open(path)


data = codecs.open("C:\Users\demreis3\Documents\smartcities_badhersfeld\data\BDHData\0ab9938e-0aa9-49cd-b9b5-68b77e6a97eb.txt", "r", encoding="utf-8")

import pickle
reader = pickle.load(open('C:\Users\demreis3\Documents\smartcities_badhersfeld\data\BDHData\0ab9938e-0aa9-49cd-b9b5-68b77e6a97eb.txt'))
reader.readline()

df = pandas.read_table('C:\Users\demreis3\Documents\smartcities_badhersfeld\data\BDHData\0ab9938e-0aa9-49cd-b9b5-68b77e6a97eb.txt', sep=',', header=None)

with open('C:\Users\demreis3\Documents\smartcities_badhersfeld\data\BDHData\0ab9938e-0aa9-49cd-b9b5-68b77e6a97eb') as json_data:
   obj = json.load(json_data)
   frame = pd.DataFrame(obj['statementName'], columns=['lng', 'type','measurement','lat','sensorId','timestamp','SID','eventType'])