import paho.mqtt.client as mqtt
import sys

MQTT_ADDRESS = '0.0.0.0'
MQTT_USER = 'mosquitong'
MQTT_PASSWORD = 'elong-mosquitong'
MQTT_TOPIC_ESP = 'esp/+'
MQTT_TOPIC_ESP1 = 'esp/ble1'
MQTT_TOPIC_ESP2 = 'esp/ble2'
MQTT_TOPIC_ESP3 = 'esp/ble3'

testssid = "wifi"

esp1rssi_nothing = []
esp2rssi_nothing = []
esp3rssi_nothing = []

esp1rssi_mobhaile = []
esp2rssi_mobhaile = []
esp3rssi_mobhaile = []


esp1av = 0
esp2av = 0
esp3av = 0

nothing_file = open(sys.argv[1], "w")
mobhaile_file = open(sys.argv[2], "w")

def average(data):
    sum = 0
    for d in data:
        sum += d
    return sum / len(data)

def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC_ESP)


def on_message(client, userdata, msg):
    payload = str(msg.payload)[2::][::-1][1::][::-1].strip()
    print(payload)
    for ble in payload.split(':'):
        if ble == ' ' or ble == '':
            continue
        namerssi = str(ble).split(',')
        name = namerssi[0].strip()
        rssi = int(namerssi[1].strip())
        if msg.topic ==  MQTT_TOPIC_ESP1:
            if name == "nothing":
                esp1rssi_nothing.append(rssi)
                nothing_file.write(f"esp1: {rssi} \n")
            elif name == "mobhaile":
                esp1rssi_mobhaile.append(rssi)
                mobhaile_file.write(f"esp1: {rssi} \n")

        elif msg.topic ==  MQTT_TOPIC_ESP2:
            if name == "nothing":
                esp2rssi_nothing.append(rssi)
                nothing_file.write(f"esp2: {rssi} \n")
            elif name == "mobhaile":
                esp2rssi_mobhaile.append(rssi)
                mobhaile_file.write(f"esp2: {rssi} \n")

        
        elif msg.topic ==  MQTT_TOPIC_ESP3:
            if name == "nothing":
                esp3rssi_nothing.append(rssi)
                nothing_file.write(f"esp3: {rssi} \n")
            elif name == "mobhaile":
                esp3rssi_mobhaile.append(rssi)
                mobhaile_file.write(f"esp3: {rssi} \n")



    print("nothing: {} {} {} \nmobhaile {} {} {}".format(esp1rssi_nothing, esp2rssi_nothing, esp3rssi_nothing, esp1rssi_mobhaile, esp2rssi_mobhaile, esp3rssi_mobhaile))
    


def main():
    



    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.connect(MQTT_ADDRESS, 1883, 60)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    main()
