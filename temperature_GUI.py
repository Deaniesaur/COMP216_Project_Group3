# COMP216 W2022 | SEC.001 - Group 3
# Final Project - Publisher
# April 16, 2022
# Participants:
# Alvarado, Bernadette
# Ariza Bustos, Luz
# De Guzman, Marc Louis Gene
# Duquinal, Apple Coleene
# Pinlac, Dean Carlo
# Non-Participants:
# None
import json
import string
import threading
import random
from tkinter import *
from tkinter import Tk, Canvas, Frame, W
from tkinter import messagebox
from tkinter.ttk import *
import argparse
import time, sys
from matplotlib.pyplot import flag
import paho.mqtt.client as mqtt
from publisher import Publisher

from group_3_roomtemp_generator import RoomTemp

flag_status = False

class RoomTempGUI(Tk):
  sensors_address = {
    "LivingRoom": "123.89.46.72",
    "Kitchen": "123.89.46.44",
    "Bath Room": "123.89.46.56",
    "Mater Bedroom": "123.89.46.98",
    "Dinning Room": "123.89.46.34",
    "Play Room": "123.89.46.65",
    "Laundry": "123.89.46.89"
  }

  def __init__(self, topic_name):
    super().__init__()
    self.title('Room Temperature Publisher')
    self.__topic = topic_name

    # Initialize UI
    self.create_vars()
    self.create_ui()
    self.configureResizable()

  def configureResizable(self):
    row_index = 0
    col_index = 0
    max_row = 10 # we have maximum 10 rows
    max_col = 2 # we have maximume 2 columns

    while row_index < max_row:
      Grid.rowconfigure(self, index=row_index, weight=1)
      row_index += 1

    # while col_index < max_col:
    #   Grid.columnconfigure(self, index=col_index, weight=1)
    #   Grid.columnconfigure(self, index=col_index, weight=1)
    #   col_index += 1
    Grid.columnconfigure(self, index=0, weight=1)
    Grid.columnconfigure(self, index=1, weight=3)

  def create_vars(self):
    self.__flag_status = False
    self.__name = StringVar()
    self.__time = StringVar()
    self.__base = StringVar()
    self.__min = StringVar()
    self.__max = StringVar()
    self.__delta = StringVar()
    self.__min_step = StringVar()
    self.__max_step = StringVar()
    self.__min_cycle = StringVar()
    self.__max_cycle = StringVar()
    self.__squiggle = BooleanVar()
    self.__button_name = StringVar(value='Start')
    self.__status = StringVar(value='Standby')

    # dropdown options
    self.__minMaxValues = [18, 18.5, 19, 19.5, 20, 20.5, 21]
    self.__stepsValues = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    self.__cycleValues = [1, 2, 3, 4]
    self.__sensors_name = ["LivingRoom", "Kitchen", "Bath Room", "Mater Bedroom", "Dinning Room", "Play Room", "Laundry"]
    self.__time_intervals = [0.25, 0.5, 1, 1.5, 2, 2.5]

  def create_ui(self, parent=None):
    if not parent:
      parent = self

    Label(
      parent,
      text='Publisher Parameters',
      font=('Arial Bold', 14),
      anchor='c',
      justify='center',
    ).grid(row=0, columnspan=2, sticky='nsew', pady=(20, 10)) # form title

    Label(parent, text='Sensor Name:', font=('Arial', 10), anchor='w').grid(row=1, column=0, sticky='nsew', pady=(0, 5), padx=(3,0))
    Label(parent, text='Time Interval (seconds):', font=('Arial', 10), anchor='w').grid(row=2, column=0, sticky='nsew', pady=(0, 5), padx=(3, 0))
    Label(parent, text='Starting Temp:', font=('Arial' ,10), anchor='w').grid(row=3, column=0, sticky='nsew', pady=(0, 5), padx=(3,0))
    Label(parent, text='Minimum Temp:', font=('Arial' ,10), anchor='w').grid(row=4, column=0, sticky='nsew', pady=(0, 5), padx=(3,0))
    Label(parent, text='Max Temp:', font=('Arial' ,10), anchor='w').grid(row=5, column=0, sticky='nsew', pady=(0, 5), padx=(3,0))
    Label(parent, text='Delta (Range: -1-1):', font=('Arial' ,10), anchor='w').grid(row=6, column=0, sticky='nsew', pady=(0, 5), padx=(3,0))
    Label(parent, text='Min Step:', font=('Arial' ,10), anchor='w').grid(row=7, column=0, sticky='nsew', pady=(0, 5), padx=(3,0))
    Label(parent, text='Max Step:', font=('Arial' ,10), anchor='w').grid(row=8, column=0, sticky='nsew', pady=(0, 5), padx=(3,0))
    Label(parent, text='Min Cycle:', font=('Arial' ,10), anchor='w').grid(row=9, column=0, sticky='nsew', pady=(0, 5), padx=(3,0))
    Label(parent, text='Max Cycle:', font=('Arial' ,10), anchor='w').grid(row=10, column=0, sticky='nsew', pady=(0, 5), padx=(3,0))
    Label(parent, text='Squiggle:', font=('Arial' ,10), anchor='w').grid(row=11, column=0, sticky='nsew', pady=(0, 5), padx=(3,0))


    # create base combobox
    nameComboBox = Combobox(parent, width=20, textvariable=self.__name)
    nameComboBox['values'] = self.__sensors_name
    # set default
    nameComboBox.current(5)
    nameComboBox.grid(row=1, column=1, sticky='W', pady=(0, 1))

    # create base combobox
    timeComboBox = Combobox(parent, width=20, textvariable=self.__time)
    timeComboBox['values'] = self.__time_intervals
    # set default
    timeComboBox.current(2)
    timeComboBox.grid(row=2, column=1, sticky='W', pady=(0, 1))

    # create base combobox
    minComboBox = Combobox(parent, width=20, textvariable=self.__base)
    minComboBox['values'] = self.__minMaxValues
    # set default to 18.5
    minComboBox.current(1)
    minComboBox.grid(row=3, column=1, sticky='W', pady=(0, 5))

    # create min combobox
    minComboBox = Combobox(parent, width=20, textvariable=self.__min)
    minComboBox['values'] = self.__minMaxValues
    # set default to min
    minComboBox.current(0)
    minComboBox.grid(row=4, column=1, sticky='W', pady=(0, 5))

    # create max combobox
    maxComboBox = Combobox(parent, width=20, textvariable=self.__max)
    maxComboBox['values'] = self.__minMaxValues
    # set default to max
    maxComboBox.current(6)
    maxComboBox.grid(row=5, column=1, sticky='W', pady=(0, 5))

    e = Entry(
      parent,
      textvariable=self.__delta,
      width=23
    )
    e.insert(0, '1')
    e.grid(
        row=6,                      # goes into the 6th row
        column=1,                    # goes into the second column
        sticky=W,                   # must be aligned to the left
        pady=(0, 5))

    # create min step combobox
    minStepComboBox = Combobox(parent, width=20, textvariable=self.__min_step)
    minStepComboBox['values'] = self.__stepsValues
    # set default to min step
    minStepComboBox.current(0)
    minStepComboBox.grid(row=7, column=1, sticky='W', pady=(0, 5))

    # create max step combobox
    maxStepComboBox = Combobox(parent, width=20, textvariable=self.__max_step)
    maxStepComboBox['values'] = self.__stepsValues
    # set default to max step
    maxStepComboBox.current(6)
    maxStepComboBox.grid(row=8, column=1, sticky='W', pady=(0, 5))

    # create min cycle
    minCycleComboBox = Combobox(parent, width=20, textvariable=self.__min_cycle)
    minCycleComboBox['values'] = self.__cycleValues
    # set default min cycle
    minCycleComboBox.current(0)
    minCycleComboBox.grid(row=9, column=1, sticky='W', pady=(0, 5))

    # create max cycle
    maxCycleComboBox = Combobox(parent, width=20, textvariable=self.__max_cycle)
    maxCycleComboBox['values'] = self.__cycleValues
    # set default max cycle
    maxCycleComboBox.current(3)
    maxCycleComboBox.grid(row=10, column=1, sticky='W', pady=(0, 5))

    # create radio button for squiggle
    trueSquiggleRadioBtn = Radiobutton(
                      parent, 
                      text='True',
                      value=True,
                      variable=self.__squiggle)
    falseSquiggleRadioBtn = Radiobutton(
                      parent, 
                      text='False',
                      value=False,
                      variable=self.__squiggle)
    
    # default squiggle
    self.__squiggle.set('false')

    trueSquiggleRadioBtn.grid(row=11, column=1, columnspan=2, sticky=W, pady=(0, 5))
    falseSquiggleRadioBtn.grid(row=12, column=1, columnspan=2, sticky=W, pady=(0, 5))

    Button(parent, textvariable=self.__button_name, width=18, command=self.btn_click).grid(row=13, column=0, padx=3, pady=(0, 10))
    Label(parent, textvariable=self.__status, width=30).grid(row=13, column=1, padx=3, pady=(0, 10))

  def btn_click(self):
    if self.__button_name.get() == 'Start':
      self.__button_name.set('Stop')
      self.__flag_status = True
      # parse values to float for validation
      parsedBase = float(self.__base.get())
      parsedMin = float(self.__min.get())
      parsedMax = float(self.__max.get())
      parsedMinStep = float(self.__min_step.get())
      parsedMaxStep = float(self.__max_step.get())
      parsedMinCycle = int(self.__min_cycle.get())
      parsedMaxCycle = int(self.__max_cycle.get())
      parsedName = self.__name.get()
      parsedInterval = float(self.__time.get())

      # if blank delta entry
      if not self.__delta.get().strip():   
        messagebox.showinfo(title='Information', message="Please enter delta value")
        return
      
      # input may be invalid valid values are -1 to 1
      try:
        parsedDelta = float(self.__delta.get())
        if(parsedDelta < -1 or parsedDelta > 1):
          messagebox.showinfo(title='Information', message="Delta must be from -1 to 1")
          return
      except Exception as e:
        parseErroMsg = f'Error parsing input: {e}'
        messagebox.showinfo(title='Information', message=parseErroMsg)
        return

      if (parsedMaxCycle <= parsedMinCycle):
        messagebox.showinfo(title='Information', message="Max cycle must be greater than min cycle")
        return

      print(f'topic name: {self.__topic}')
      print(f'base: {parsedBase}\nmin: {parsedMin}\nmax: {parsedMax}\ndelta: {parsedDelta}\nmin_step: {parsedMinStep}\nmax_step: {parsedMaxStep}')
      print(f'min cycle: {parsedMinCycle}\nmax cycle: {parsedMaxCycle}\nsquiggle: {self.__squiggle.get()}')

      thread = threading.Thread(
        target=self.run,
        args=[parsedBase, parsedMin, parsedMax, parsedDelta, parsedMinStep, parsedMaxStep, parsedMinCycle, parsedMaxCycle, parsedName, parsedInterval])
      thread.setDaemon(True)
      thread.start()
    
    else:
      self.__button_name.set('Start')
      self.__status.set('Standby')
      self.__flag_status = False

  def run(self, parsedBase, parsedMin, parsedMax, parsedDelta, parsedMinStep, parsedMaxStep, parsedMinCycle, parsedMaxCycle, parsedName, parsedInterval):
    # generate room temperature
    tempGenerator = RoomTemp(base=parsedBase,
      min=parsedMin, max=parsedMax, delta=parsedDelta,
      min_step=parsedMinStep, max_step=parsedMaxStep, min_cycle=parsedMinCycle, max_cycle=parsedMaxCycle,
      squiggle=self.__squiggle.get())
    publisher = Publisher()
    miss_transmission = 0
    rand_int = 0
    while self.__flag_status:
      wild = random.randint(5, 10)
      wild_data = random.randint(1, 100)
      # miss transmission
      if rand_int == 0:
        rand_int = random.randint(1, 100)
      if miss_transmission == 100:
        rand_int = 0
        miss_transmission = 0
      if miss_transmission == rand_int:
        miss_transmission += 1
        print('----------------------------\n\nData not sent, -- miss transmission --\n\n---------------------------- ')
        time.sleep(parsedInterval)
        continue

      temp = tempGenerator.getTemp()
      # wild data
      if wild_data == rand_int:
        temp = temp * wild
        print('----------------------------\n\n *********** Wild Data ***********\n\n---------------------------- ')

      try:
        # Create payload data
        packetId = int(time.time() * 1000)
        msg_dict = {
          "packetId": packetId,
          "name": parsedName,
          "temp": temp,
          "macAddress": self.sensors_address[parsedName],
        }
        # Convert to string
        data = json.dumps(msg_dict, indent=4, sort_keys=True, default=str)
        # Publish on a topic
        publisher.publish(topic=self.__topic, payload=data, qos=0)
        print('Published msg: {}'.format(msg_dict))
        self.__status.set(f'Packet Sending: {msg_dict["packetId"]}')
        # Increment published cycle count
        # Sleep loop for 5 secs
        time.sleep(parsedInterval)

      except (KeyboardInterrupt, SystemExit):
        mqtt.DISCONNECT()
        sys.exit()
      miss_transmission += 1
    # Disconnect from Mqtt broker
    publisher.disconnect()

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--topic", help="Topic name", required=True, type=str)
  args = parser.parse_args()
  rmPub = RoomTempGUI(topic_name=args.topic)
  rmPub.geometry("400x300")
  rmPub.minsize(width=450, height=400)
  rmPub.mainloop()
