import paho.mqtt.client as mqtt


class Publisher:
    # Create Mqtt client
    mqttc = mqtt.Client()

    def on_connect(self, mqttc, userdata, flags, rc):
        print('Connected.. \n Return code: ' + str(rc))

    def on_disconnect(self, mqttc, userdata):
        print('disconnected..')

    def on_message(self, mqttc, userdata, msg):
        print('"\n------ Received Message ------\n"')
        print('Topic: ' + msg.topic + + ', Message: ' + str(msg.payload))

    def on_publish(self, mqttc, userdata):
        print('Message published')

    def publish(self, topic, payload, qos=0):
        self.mqttc.publish(topic=topic, payload=payload, qos=qos)
        return

    def disconnect(self):
        self.mqttc.disconnect()

    # Register callbacks
    mqttc.on_connect = on_connect
    mqttc.on_disconnect = on_disconnect
    mqttc.on_message = on_message
    mqttc.on_publish = on_publish

    # Connect to Mqtt broker on specified host and port
    mqttc.connect(host='localhost', port=1883)
