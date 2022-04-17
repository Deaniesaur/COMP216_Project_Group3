# COMP216 W2022 | SEC.001 - Group 3
# Lab Assignment 11 - Publish / Subscribe
# April 6, 2022
# Participants:
# Alvarado, Bernadette
# Ariza Bustos, Luz
# De Guzman, Marc Louis Gene
# Duquinal, Apple Coleene
# Pinlac, Dean Carlo
# Non-Participants:
# None

import json
import paho.mqtt.client as mqtt
import group_3_utils

# def on_connect(mqttc, userdata, flags, rc):
#     print('Connected.. \n Return code: ' + str(rc))
#     mqttc.subscribe(topic='network/#', qos=0)

# def on_disconnect(mqrrc, userdata, rc):
#     print('Disconnected.. \n Return code: ' + str(rc))

# def on_message(mqttc, userdata, msg):
#     print('"\n------ Received Message ------\n"')
#     print('Topic: ' + msg.topic + ', Message: ' + str(msg.payload))
#     decode_msg(msg.payload)

# def on_subscribe(mqttc, userdata, mid, granted_qos):
#     print('Subscribed')

# def on_unsubscribed(mqttc, userdata, mid, granted_qos):
#     print('Unsubscribed')

# # Decode received message
# def decode_msg(msg):
#     msg = msg.decode('utf-8')
#     payload = json.loads(msg)
#     print("\n------ Decoded Message ------\n")
#     group_3_utils.print_data(payload)

# # Create Mqtt client
# mqttc = mqtt.Client()

# # Register callbacks
# mqttc.on_connect = on_connect
# mqttc.on_disconnect = on_disconnect
# mqttc.on_message = on_message
# mqttc.on_subscribe = on_subscribe
# mqttc.on_unsubscribe = on_unsubscribed

# # Connect to Mqtt broker on specified host and port
# mqttc.connect(host='localhost', port=1883)

# # Run client forever
# mqttc.loop_forever()