import wiringpi
import MAX6675
import math
import time

def bubbleSort (temp, size):
  for i in range(1, size):
    for j in range(0, size-1):
      if temp[j] > temp[j+1]:
        hold = temp[j]
        temp[j] = temp[j+1]
        temp[j+1] = hold

def aveTemp(temp, size):
  flag = 1
  ave  = 0.0
  tol  = 2
  
  while flag == 1:
    bubbleSort(temp, size)
    sum = 0.0
    for i in range(1, size-1):
      sum = sum + temp[i]
    ave = sum/(size-2)
    if math.fabs(temp[0]) < (math.fabs(ave) - tol):
      temp[0] = ave
    elif math.fabs(temp[size-1]) > (math.fabs(ave) + tol):
      temp[size-1] = ave
    else:
      flag = 0
  return ave
  
def readTemp(CS_pin, SO_pin, SCK_pin, units,size):
  temp = []
  for i in range(0, size):
    temp.append(MAX6675.readTemp(CS_pin, SO_pin, SCK_pin, units))
  T = aveTemp(temp,size)
  time.sleep(1)
  return T