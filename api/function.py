import requests
import json
from datetime import datetime
import os
from django.conf import settings
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

class API:

    url1 = 'http://api.openweathermap.org/data/2.5/weather?appid=f6182a9874fa6e1a215f5a7489f8b3eb&q='

    def getcity1JSON(self, city1):
        url = self.url1+city1
        data = requests.get(url).json()
        res = {}
        res['City'] = city1
        res['Temperature'] = "{0:.2f}".format(float(data['main']['temp'])- 273.15) 
        res['timestamp'] = str(datetime.now())
        self.amazon(res)
        return res
    
    def amazon(self, data):
        myMQTTClient = AWSIoTMQTTClient("Temp_sensor")
        myMQTTClient.configureEndpoint("a3afa41mc06g6e.iot.us-west-2.amazonaws.com", 8883)
        myMQTTClient.configureCredentials(os.path.join(settings.ROOT_PATH, 'root-CA.crt'),os.path.join(settings.ROOT_PATH, 'Temp_sensor.private.key'),
                                          os.path.join(settings.ROOT_PATH, 'Temp_sensor.cert.pem'))
        print('start connection')
        myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        myMQTTClient.configureConnectDisconnectTimeout(1000)  # 10 sec
        myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
        myMQTTClient.connect()
        print('connected')
        myMQTTClient.publish("Temp_sensor/info", "connected", 0)
        payload = json.dumps(data)
        myMQTTClient.publish("Temp_sensor/data", payload, 0)








