import paho.mqtt.client as mqtt

MQTT_ADDRESS = '192.168.43.134'
MQTT_USER = 'mosquitong'
MQTT_PASSWORD = 'elong-mosquitong'
MQTT_TOPIC_ESP = 'esp/+'
MQTT_TOPIC_ESP1 = 'esp/rec1'
MQTT_TOPIC_ESP2 = 'esp/rec2'
MQTT_TOPIC_ESP3 = 'esp/rec3'

esp1data = {}
esp2data = {}
esp3data = {}


def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC_ESP)


def on_message(client, userdata, msg):
    payload = str(msg.payload)[2::][::-1][1::][::-1]
    for wifi in payload.split(';'):
        if wifi == ' ':
            continue
        ssidrssi = str(wifi).split(':')
        ssid = ssidrssi[0].strip()
        rssi = int(ssidrssi[1].strip())
        if msg.topic == MQTT_TOPIC_ESP1:
            esp1data[ssid] = rssi
            if ssid == "wifi":
                print("esp1:", end=" ")
                print(rssi)
        elif msg.topic == MQTT_TOPIC_ESP2:
            esp2data[ssid] = rssi
            if ssid == "wifi":
                print("esp2:", end=" ")
                print(rssi)
        elif msg.topic == MQTT_TOPIC_ESP3:
            esp3data[ssid] = rssi
            if ssid == "wifi":
                print("esp3:", end=" ")
                print(rssi)


def main():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.connect(MQTT_ADDRESS, 1883, 60)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    main()
