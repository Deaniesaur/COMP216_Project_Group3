# COMP216 W2022 | SEC.001 - Group 3 
# Lab Assignment 6 - Data Generator
# March 23, 2022
# Participants:
# Alvarado, Bernadette
# Ariza Bustos, Luz
# De Guzman, Marc Louis Gene
# Duquinal, Apple Coleene
# Pinlac, Dean Carlo
# Non-Participants:
# None

# Temp Generator
# Optional Attributes: (9)
# --base, --min, --max, --min_step, --max_step,
# --delta, --min_cycle, --max_cycle, --squiggle

from email.mime import base
import random
from unicodedata import decimal
import matplotlib.pyplot as plt
import argparse

class RoomTemp():
  def __init__(self, base=18.5, min=18, max=21, delta=0.08, min_step=0, max_step=0.6, min_cycle=1, max_cycle=4, squiggle=False):
    random.seed("COMP216Group3")
    self.__base = base
    self.__min = min
    self.__max = max
    self.__range = max_step - min_step
    print('range', self.__range)
    self.__delta = delta
    self.__min_step = min_step if delta > 0 else min_step * -1
    self.__max_step = max_step if delta > 0 else max_step * -1
    self.__min_cycle = min_cycle
    self.__max_cycle = max_cycle
    self.__cycle = random.randint(self.__min_cycle, self.__max_cycle)
    self.__half = self.__cycle / 2
    self.__squiggle = True if squiggle == 'True' else False

  def __generate(self):
    return random.random()

  def getTemp(self):
    value = self.__generate()

    # Decrease Cycle every new Temp
    self.__cycle -= 1
    if self.__cycle < 0:
      self.__reset()
    
    # Calculate Next Temp
    increment = (value * self.__delta * 5) + self.__min_step
    increment = self.__max_step if (abs(increment) > abs(self.__max_step)) else increment
    if self.__squiggle and self.__cycle == self.__half: increment *= -1
    self.__base += increment

    # Clip to Max
    if self.__base > self.__max:
      self.__base = self.__max
      self.__reset()
    
    # Clip to Min
    if self.__base < self.__min:
      self.__base = self.__min
      self.__reset()

    return self.__base
  
  def __reset(self):
    self.__cycle = random.randint(self.__min_cycle, self.__max_cycle)
    self.__half = self.__cycle / 2
    self.__delta *= -1
    self.__min_step *= -1
    self.__max_step *= -1

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--base", help="Starting Temp", type=float, default=18.5)
  parser.add_argument("--min", help="Minimum Temp", type=float, default=18)
  parser.add_argument("--max", help="Maximum Temp", type=float, default=21)
  parser.add_argument("--min_step", help="Minimum Step", type=float, default=0)
  parser.add_argument("--max_step", help="Maximum Step", type=float, default=0.6)
  parser.add_argument("--delta",
    help="Delta / Step Multiplier, Positive for 1st step increase, Negative for 1st step decrease",
    type=float,
    default=0.08)
  parser.add_argument("--min_cycle", help="Minimum Cycle", type=int, default=1)
  parser.add_argument("--max_cycle", help="Maximum Cycle", type=int, default=4)
  parser.add_argument("--squiggle", help="True if you want more squiggle, False by default", choices=['True', 'False'], default='False')

  args = parser.parse_args()
  no_of_data = 500
  print(args)
  if(args.min_step > 1 or args.min_step < 0):
    raise Exception("--min_step must be 0 to 1")

  if(args.max_step < 0):
    raise Exception("--max_step must be greater than 0")

  if(args.delta < -1 or args.delta > 1):
    raise Exception("--delta must be from -1 to 1.")

  if(args.min_cycle < 1):
    raise Exception("--min_cycle must be greater than 0")

  if(args.max_cycle <= args.min_cycle):
    raise Exception("--max_cycle must be greater than --min_cycle: " + args.min_cycle)

  tempGen = RoomTemp(args.base, args.min, args.max, args.delta, args.min_step, args.max_step, args.min_cycle, args.max_cycle, args.squiggle)
  count = range(no_of_data)
  temps = [tempGen.getTemp() for _ in range(no_of_data)]
  plt.plot(count, temps)
  plt.title("Temperature Data Generator")
  plt.ylabel("Temperature")
  plt.show()