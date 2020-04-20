#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sippy import * 
from control import * 
from pylab import *

# Tiempo de muestreo
Ts = 10

# Load data from file
f = file("identify_lower_resistor_1.csv","r")
f.readline()
# discard first samples
for _ in range(145):
  f.readline()

temp = []
u = []
e = []
low = []
up = []
for line in f.readlines():
  data = line.split(",")
  temp.append(float(data[1]))
  u.append(.44*float(data[6]))  
  # ~ e.append(float(data[3]))  
  # ~ low.append(float(data[6]))  
  # ~ up.append(float(data[7]))  
f.close()

temp1 = temp[40:365]
temp2 = temp[610:1050]
temp3 = temp[1260:-1]

img = figure(figsize=(6,5))

plot(temp1)
hold(True)
plot(temp2)
plot(temp3)

grid(True)
ylabel('Temperatura(Grados)/Potencia')
xlabel('Tiempo')
title('Temepratura del horno vs tiempo')

img.savefig('exp_fit.png')

Ta = 28

y1 = log(array(temp1) - Ta)
t1 = r_[0:10*size(temp1):10]

y2 = log(array(temp2) - Ta)
t2 = r_[0:10*size(temp2):10]

y3 = log(array(temp3) - Ta)
t3 = r_[0:10*size(temp3):10]

img = figure(figsize=(6,5))
plot(t1,y1,t2,y2,t3,y3)

grid(True)
ylabel('y')
xlabel('Tiempo')
title('Interpolador')

img.savefig('lineas.png')

p1 = polyfit(t1,y1,1)
c1 = -p1[0]
T1 = Ta + exp(p1[1])
print(c1,T1,temp1[0])

p2 = polyfit(t2,y2,1)
c1 = -p2[0]
T1 = Ta + exp(p2[1])
print(c1,T1,temp2[0])

p3 = polyfit(t3,y3,1)
c1 = -p3[0]
T1 = Ta + exp(p3[1])
print(c1,T1,temp3[0])
