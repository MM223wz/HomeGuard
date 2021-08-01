# Simple MQTT-based data collection client for the Kaa IoT platform
# See https://docs.kaaiot.io/KAA/docs/current/Tutorials/getting-started/collecting-data-from-a-device/.
# Adapted for Pycom MicroPython
import ujson as json
import machine
import utime as time
from uos import urandom as random
import _keys as keys

class DataCollectionClient:

    def __init__(self, client):
        self.client = client
        #self.client.set_callback(self.sub_cb)
        self.data_collection_topic = 'kp1/{}/dcx/{}/json'.format(keys.KAA_APP_VERSION_NAME, keys.KAA_ENDPOINT_TOKEN)
        print('Initialized MQTT Client with topic: {}'.format(self.data_collection_topic))

    def sub_cb(topic, msg):
        print(msg)

    def connect_to_server(self):
        print('Connecting to Kaa server at {}:{} using application version {} and endpoint token {}'.format(keys.MQTT_CLIENT, keys.MQTT_PORT, keys.KAA_APP_VERSION_NAME, keys.KAA_ENDPOINT_TOKEN))
        self.client.connect()
        #self.client.subscribe(topic=self.data_collection_topic)
        print('Successfully connected')

    def disconnect_from_server(self):
        print('Disconnecting from Kaa server at {}:{}...'.format(keys.MQTT_CLIENT, keys.MQTT_PORT))
        self.client.disconnect()
        print('Successfully disconnected')

    def compose_data(self, temperature, humidity):
        return json.dumps({
            'timestamp': time.localtime(),
            'temperature': temperature,
            'humidity': humidity,
            'board-temp': ((machine.temperature() - 32) / 1.8)
        })

    def compose_data_sample(self):
        return json.dumps({
            'timestamp': time.localtime(),
            'temperature': (random(1)[0] / 256 * 10) + 15,
            'humidity': (random(1)[0] / 256 * 25) + 35,
            'board-temp': ((machine.temperature() - 32) / 1.8)
        })
