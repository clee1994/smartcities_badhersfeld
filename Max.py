import globe, os

# Create dataframe for NoiseData


os.chdir(r'C:\Users\demreis3\Documents\smartcities_badhersfeld\data\BadHersfeldNoise')

filename = []
for file in glob.glob("*"):
   filename.append(file)

NoiseData = pd.DataFrame()

filename_length = len(filename)

for i in range(filename_length):
   with open(filename[i]) as json_data:
      rowdata = json.load(json_data)
      frame = pd.DataFrame(rowdata['sensordata'],columns=['lng', 'type', 'measurement', 'lat', 'sensorId', 'timestamp', 'SID', 'eventType'])
      NoiseData = NoiseData.append(frame)

# Create DataFrame for Polution DataSet


path = r'C:\Users\demreis3\Documents\smartcities_badhersfeld\data\BDHData'
os.chdir(path)

filename2 = []
for file in glob.glob("*"):
   filename.append(file)


PolutionData = pd.DataFrame()

filename_length = len(filename)