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

import string
from tkinter import *
from tkinter import Tk, Canvas, Frame, W
from tkinter import messagebox
from tkinter.ttk import *
import argparse

from group_3_roomtemp_generator import RoomTemp

class RoomTempPublisher(Tk):
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
    self.__base = StringVar()
    self.__min = StringVar()
    self.__max = StringVar()
    self.__delta = StringVar()
    self.__min_step = StringVar()
    self.__max_step = StringVar()
    self.__min_cycle = StringVar()
    self.__max_cycle = StringVar()
    self.__squiggle = BooleanVar()

    # dropdown options
    self.__minMaxValues = [18, 18.5, 19, 19.5, 20, 20.5, 21]
    self.__stepsValues = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    self.__cycleValues = [1, 2, 3, 4]
  
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

    Label(parent, text='Starting Temp:', font=('Arial' ,10), anchor='w').grid(row=1, column=0, sticky='nsew', pady=(0, 5), padx=(3,0))
    Label(parent, text='Minimum Temp:', font=('Arial' ,10), anchor='w').grid(row=2, column=0, sticky='nsew', pady=(0, 5), padx=(3,0))
    Label(parent, text='Max Temp:', font=('Arial' ,10), anchor='w').grid(row=3, column=0, sticky='nsew', pady=(0, 5), padx=(3,0))
    Label(parent, text='Delta:', font=('Arial' ,10), anchor='w').grid(row=4, column=0, sticky='nsew', pady=(0, 5), padx=(3,0))
    Label(parent, text='Min Step:', font=('Arial' ,10), anchor='w').grid(row=5, column=0, sticky='nsew', pady=(0, 5), padx=(3,0))
    Label(parent, text='Max Step:', font=('Arial' ,10), anchor='w').grid(row=6, column=0, sticky='nsew', pady=(0, 5), padx=(3,0))
    Label(parent, text='Min Cycle:', font=('Arial' ,10), anchor='w').grid(row=7, column=0, sticky='nsew', pady=(0, 5), padx=(3,0))
    Label(parent, text='Max Cycle:', font=('Arial' ,10), anchor='w').grid(row=8, column=0, sticky='nsew', pady=(0, 5), padx=(3,0))
    Label(parent, text='Squiggle:', font=('Arial' ,10), anchor='w').grid(row=9, column=0, sticky='nsew', pady=(0, 5), padx=(3,0))

    # create base combobox
    minComboBox = Combobox(parent, width=20, textvariable=self.__base)
    minComboBox['values'] = self.__minMaxValues
    # set default to 18.5
    minComboBox.current(1)
    minComboBox.grid(row=1, column=1, sticky='W', pady=(0, 5))

    # create min combobox
    minComboBox = Combobox(parent, width=20, textvariable=self.__min)
    minComboBox['values'] = self.__minMaxValues
    # set default to min
    minComboBox.current(0)
    minComboBox.grid(row=2, column=1, sticky='W', pady=(0, 5))

    # create max combobox
    maxComboBox = Combobox(parent, width=20, textvariable=self.__max)
    maxComboBox['values'] = self.__minMaxValues
    # set default to max
    maxComboBox.current(6)
    maxComboBox.grid(row=3, column=1, sticky='W', pady=(0, 5))

    Entry(
    parent, 
    textvariable=self.__delta,
    width=23
    ).grid(
        row=4,                      # goes into the 4th row
        column=1,                   # goes into the second column
        sticky=W,                   # must be aligned to the left
        pady=(0, 5))

    # create min step combobox
    minStepComboBox = Combobox(parent, width=20, textvariable=self.__min_step)
    minStepComboBox['values'] = self.__stepsValues
    # set default to min step
    minStepComboBox.current(0)
    minStepComboBox.grid(row=5, column=1, sticky='W', pady=(0, 5))

    # create max step combobox
    maxStepComboBox = Combobox(parent, width=20, textvariable=self.__max_step)
    maxStepComboBox['values'] = self.__stepsValues
    # set default to max step
    maxStepComboBox.current(6)
    maxStepComboBox.grid(row=6, column=1, sticky='W', pady=(0, 5))

    # create min cycle
    minCycleComboBox = Combobox(parent, width=20, textvariable=self.__min_cycle)
    minCycleComboBox['values'] = self.__cycleValues
    # set default min cycle
    minCycleComboBox.current(0)
    minCycleComboBox.grid(row=7, column=1, sticky='W', pady=(0, 5))

    # create max cycle
    maxCycleComboBox = Combobox(parent, width=20, textvariable=self.__max_cycle)
    maxCycleComboBox['values'] = self.__cycleValues
    # set default max cycle
    maxCycleComboBox.current(3)
    maxCycleComboBox.grid(row=8, column=1, sticky='W', pady=(0, 5))

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

    trueSquiggleRadioBtn.grid(row=9, column=1, columnspan=2, sticky=W, pady=(0, 5))
    falseSquiggleRadioBtn.grid(row=10, column=1, columnspan=2, sticky=W, pady=(0, 5))

    Button(parent, text='Publish', width=18, command=self.btnPublish_onClick).grid(row=11, column=0, padx=3, pady=(0, 10))
    Button(parent, text='Exit', command=self.destroy, width=18).grid(row=11, column=1, padx=3, pady=(0, 10))
  
  def btnPublish_onClick(self):
    print('clicked publish')
    # parse values to float for validation
    parsedBase = float(self.__base.get())
    parsedMin = float(self.__min.get())
    parsedMax = float(self.__max.get())
    parsedMinStep = float(self.__min_step.get())
    parsedMaxStep = float(self.__max_step.get())
    parsedMinCycle = int(self.__min_cycle.get())
    parsedMaxCycle = int(self.__max_cycle.get())

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

    # generate room temperature
    tempGenerator = RoomTemp(base=parsedBase,
      min=parsedMin, max=parsedMax, delta=parsedDelta,
      min_step=parsedMinStep, max_step=parsedMaxStep, min_cycle=parsedMinCycle, max_cycle=parsedMaxCycle,
      squiggle=self.__squiggle.get())
    
    print(f'Generated temp: {tempGenerator.getTemp()}')

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--topic", help="Topic name", required=True, type=str)
  args = parser.parse_args()

  rmPub = RoomTempPublisher(topic_name=args.topic)
  rmPub.geometry("400x300")
  rmPub.minsize(width=450, height=400)
  rmPub.mainloop()