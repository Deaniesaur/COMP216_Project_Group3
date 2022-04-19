# COMP216 W2022 | SEC.001 - Group 3
# Lab Assignment 10 - Display Dynamic Time Series
# April 6, 2022
# Participants:
# Alvarado, Bernadette
# Ariza Bustos, Luz
# De Guzman, Marc Louis Gene
# Duquinal, Apple Coleene
# Pinlac, Dean Carlo
# Non-Participants:
# None

from tkinter import *
from tkinter import Tk, Canvas, Frame, W
from tkinter import messagebox
from tkinter.ttk import *
import paho.mqtt.client as mqtt
import json

class TempClient(Tk):
    def __init__(self):
        super().__init__()
        self.title('Group3 Dynamic Time Series - Temperature')
        self.__data = []

        # Initialize UI
        self.initUI()

        # Initialize MQTT connection
        mqttc = mqtt.Client()
        mqttc.on_connect = self.on_connect
        mqttc.on_disconnect = self.on_disconnect
        mqttc.on_message = self.on_message
        mqttc.on_subscribe = self.on_subscribe
        mqttc.on_unsubscribe = self.on_unsubscribed

        # Connect to Mqtt broker on specified host and port
        mqttc.connect(host='localhost', port=1883)
        mqttc.loop_start()

    def on_connect(self, mqttc, userdata, flags, rc):
        print('Connected.. \n Return code: ' + str(rc))
        mqttc.subscribe(topic='room_temp_1/#', qos=0)

    def on_disconnect(self, mqrrc, userdata, rc):
        print('Disconnected.. \n Return code: ' + str(rc))

    def on_message(self, mqttc, userdata, msg):
        print('"\n------ Received Message ------\n"')
        print('Topic: ' + msg.topic + ', Message: ' + str(msg.payload))
        message = json.loads(msg.payload)
        print(message)
        self.update_data(message['temp'])

    def on_subscribe(self, mqttc, userdata, mid, granted_qos):
        print('Subscribed')

    def on_unsubscribed(self, mqttc, userdata, mid, granted_qos):
        print('Unsubscribed')

    def update_data(self, newTemp):
        print('data', self.__data)
        if(len(self.__data) >= 20):
            self.__data.pop(0)

        self.__data.append(newTemp)
        
        # Method to Display Rectangles and Lines
        self.canv.delete('all')
        self.displayLines()
        self.displayData()

    def create_styles(self):
        style = Style()
        style.configure('TFrame', background='#80cc80')
        style.configure('TLabel', background='#80cc80')

    def initUI(self):
        Canvas(width=600, height=280).pack()
        container = Frame(self, padding=(5, 5))
        container.place(relx=0.015, rely=0.02, relheight=0.96, relwidth=0.97)
        Label(container, text='Temp Range: 18 - 21 only', font='Arial 12 bold').place(relx=0.33, height=30)

        # Initialize Canvas
        self.canv = Canvas(self)
        self.canv.place(relx=0.1, rely=0.24, width=500, height=180)
        
        # Initialize Start Value
        self.create_styles()

    def displayLines(self):
        self.canv = Canvas(self)
        self.canv.place(relx=0.1, rely=0.24, width=500, height=180)

        lineHeight = 10
        textDisplay = 22
        for _ in range(4):
            self.canv.create_text(25, lineHeight, anchor=W, font='Arial 7', text=textDisplay)
            self.canv.create_line(45, lineHeight, 65, lineHeight)
            self.canv.create_line(50, lineHeight+20, 65, lineHeight+20)
            lineHeight += 40
            textDisplay -= 1

        self.canv.create_text(25, lineHeight, anchor=W, font='Arial 7', text=textDisplay)
        self.canv.create_line(45, lineHeight, 65, lineHeight)

    def displayData(self):
        spacing = 70
        prevY = 0
        data_count = len(self.__data)
        for i in range(data_count):
            full = 170 - 10
            relative = (self.__data[i] - 18) / (22 - 18)
            height = 170 - (relative * full)
            
            # Line - No line if data is less than 2 counts
            if(i > 0):
                self.canv.create_line(spacing, prevY, spacing + 20, height)
            
            spacing += 20
            prevY = height

if __name__ == '__main__':
    sts = TempClient()
    sts.mainloop()