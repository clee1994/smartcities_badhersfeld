#-------------------------------------------------------------------------------
# Name:        Python sample historic data client
# Author:      Jan Grimmer
# Created:     20.03.2018
#-------------------------------------------------------------------------------

from http.client import HTTPSConnection
from base64 import b64encode
import json

HOST_STAGING = "sc-hackathon-s.urbanpulse.de"
HOST_PRODUCTION = "sc-hackathon.urbanpulse.de"
PORT_HISTORIC_DATA = 42000

USER_PW = b"hackathon:L33333t+"

def getData(host, sid, since, until):
        server = host + ":" + str(PORT_HISTORIC_DATA)

        pathTemplate = "/UrbanPulseData/historic/sensordata?since={0}&until={1}&sid={2}"
        path = pathTemplate.format(since,until,sid)

        connection = HTTPSConnection(server)
        userAndPass = b64encode(USER_PW).decode("ascii")
        headers = { 'Authorization' : 'Basic %s' %  userAndPass }

        connection.request('GET', path, headers=headers)
        response = connection.getresponse()
        data = response.read()
        return data

def main():
    host = HOST_STAGING
    # A list of all sensors can be obtained from https://<HOST>/UrbanPulseManagement/api/sensors with credentials hackathon/L33333t+
    sid = "846e9b95-a9b4-4d5f-b549-f6e211b9c3ba"
    since = "2018-03-26T11:18:00.000Z"
    until = "2018-03-26T11:22:00.000Z"

    data = getData(host, sid, since, until)
    wrappedJsonObject = json.loads(data)
    jsonArray = wrappedJsonObject['sensordata']
    for event in jsonArray:
        print("Received: " + json.dumps(event))

if __name__ == '__main__':
    main()
