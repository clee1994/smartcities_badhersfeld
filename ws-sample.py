#-------------------------------------------------------------------------------
# Name:        Python sample WSS client
# Author:      Jan Grimmer
# Created:     19.03.2018
# Required external packages from pip: websocket-client
#-------------------------------------------------------------------------------

from websocket import create_connection
from base64 import b64encode
import json
import signal
import sys

HOST_STAGING = "sc-hackathon-s.urbanpulse.de"
HOST_PRODUCTION = "sc-hackathon.urbanpulse.de"
PORT_WEBSOCKET_LIVE_DATA = 3210
USER_PW = b"hackathon:L33333t+"

STATEMENT_TRAFFIC_MANAGEMENT_RAW_EVENTS = "SwarcoTMSEventTypeEventTypeStatement";
STATEMENT_TRAFFIC_PREDICTIONS = "SPPAnalyticsStatementV2";
STATEMENT_WEATHER_DATA = "OpenWeatherMapEventTypeEventTypeStatement";
STATEMENT_ENVIRONMENT_DATA = "NRWEnvironmentEventTypeEventTypeStatement";
STATEMENT_NOISE = "WaveScapeEventTypeEventTypeStatement";

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

def connect(host, statement):
    userAndPass = b64encode(USER_PW).decode("ascii")
    headers = ["Authorization: Basic " + userAndPass ]

    url = "wss://" + host + ":" + str(PORT_WEBSOCKET_LIVE_DATA) + "/OutboundInterfaces/outbound/" + statement
    print(url)

    ws = create_connection(url, header=headers)
    while True:
        result = ws.recv()
        print("Received: " + result)

def main():
    host = HOST_STAGING
    statement = STATEMENT_TRAFFIC_MANAGEMENT_RAW_EVENTS
    signal.signal(signal.SIGINT, signal_handler)
    connect(host, statement)

if __name__ == '__main__':
    main()
