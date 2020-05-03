#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sippy import * 
from control import * 
from pylab import *
import sys

# Tiempo de muestreo
Ts = 10
def main(argv):
  fname= argv[0]
  # Load data from file
  f = file(fname,"r")
  f.readline()
  temp = []
  u = []
  e = []
  for line in f.readlines():
    data = line.split(",")
    temp.append(float(data[1]))
    u.append(float(data[6]))  
    e.append(float(data[3]))  
  f.close()

  setpoint = array(e)+array(temp)
  t = r_[0:10*len(u):10]/60.0

  img = figure(figsize=(6,5))
  plot(t,temp,t,u,t,e,t,setpoint,'--k')
  grid(True)
  xlim((0,t[-1]))
  ylabel('Temperatura(Grados)/Potencia')
  xlabel('Tiempo (min)')
  title('Temperatura del horno vs tiempo')
  legend(('Temperatura','Mando','Error'))

  img.savefig(fname+'.png')

if __name__ == "__main__":
  main(sys.argv[1:])
