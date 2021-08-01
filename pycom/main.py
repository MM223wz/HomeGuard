# HomeGuard Main code
import pycom
import utime as time
import _keys as keys
import machine
from mqtt import MQTTClient
from kaa_client import DataCollectionClient
from dht import DHT

# Adjust to your needs
READ_SENSOR_DATA_INTERVAL = 5 # in seconds

# Turn on blinking blue
pycom.heartbeat(True)

# Connect to Kaa Cloud
client = MQTTClient(machine.unique_id(), keys.MQTT_CLIENT, port=keys.MQTT_PORT)
data_collection_client = DataCollectionClient(client)
data_collection_client.connect_to_server()

# Set up DHT-11 sensor
sensor = DHT('P23', 0)

# Main program loop
while True:
    time.sleep(READ_SENSOR_DATA_INTERVAL)
    result = sensor.read()
    if result.is_valid():
        msg_data = data_collection_client.compose_data(temperature=result.temperature, humidity=result.humidity)
        data_collection_client.client.publish(topic=data_collection_client.data_collection_topic, msg=msg_data)
        print('--> Sent message on topic "{}":\n{}'.format(data_collection_client.data_collection_topic, msg_data))
