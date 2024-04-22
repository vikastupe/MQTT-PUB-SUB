import time
from paho.mqtt import client as mqtt_client
import json
import psutil
import traceback

broker = 'broker.emqx.io'
port = 1883
topic = "mqtt-server-msg"
client_id = f'publish-msg'
# username = 'emqx'
# password = 'public'

def machine_info():
    try:
        disk_info = psutil.disk_usage('/')
        machine_data = json.dumps({
            "cpu_percent": psutil.cpu_percent(interval=1),
            "logical_cpu_count": psutil.cpu_count(logical=True),
            "total_space": round(disk_info.total / (1024 ** 3), 2),
            "used_space": round(disk_info.used / (1024 ** 3), 2),
            "free_space": round(disk_info.free / (1024 ** 3), 2),
            "ram_usage": psutil.virtual_memory().percent
        })   
        return machine_data

    except Exception as e:
        traceback.print_exc()


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    
    while True:
        time.sleep(2)
        msg = machine_info()
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()
