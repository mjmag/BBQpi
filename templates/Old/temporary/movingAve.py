import math

temp = [40,39,41,38,35];
## previous temperature readings

def WeightedAve(temp, size):
  n = 10
  ave  = 0.0
  sum = 0.0
  sumt= 0.0
  if size > n:
    factor = range(n)
  else:
    factor = range(size);
  for i in range(0, size):  
    sum = sum + (factor[i]+1)* temp[i]
    sumt = sumt+(factor[i]+1)
  ave = sum/sumt
    
  return ave

def ExpAve(temp, size):
  a=0.5
  ave = 0.0
  sum = 0.0
  sumt= 0.0
  factor = range(size);
  for i in range(0, size):  
    sum = sum + (1-a)**(factor[i])* temp[size-1-i]
    sumt= sumt+ (1-a)**(factor[i])
  ave = sum/sumt

  return ave 
  ##return "%.2f" % ave
