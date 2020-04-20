#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sippy import * 
from control import * 
from pylab import *

# Tiempo de muestreo
Ts = 10

# Load data from file
f = file("step-30.csv","r")
f.readline()
# discard first samples
for _ in range(1):
  f.readline()

temp = []
u = []
e = []
low = []
up = []
for line in f.readlines():
  data = line.split(",")
  temp.append(float(data[1]))
  u.append(float(data[6]))  
  # ~ e.append(float(data[3]))  
  # ~ low.append(float(data[6]))  
  # ~ up.append(float(data[7]))  
f.close()

minTemp = temp[0]
temp = [x - minTemp for x in temp]

# Identify
#Identified_system=system_identification(temp,u,'ARX',tsample=Ts, IC='AIC')
Identified_system=system_identification(temp,u,'ARX',tsample=Ts, IC='AIC', delays=[70])
[t,y,x]=forced_response(Identified_system.G,T=r_[0:10*len(u):10],U=u)
print(Identified_system.G)
#print(ss(Identified_system.G))

# Display Data
temp = [x + minTemp for x in temp]
y = [x + minTemp for x in y]
t = [x/60. for x in t]
img = figure(figsize=(6,5))
plot(t,temp,t,u,t,y)

e = 0
for i, T in enumerate(temp):
  e += (T-y[i])**2
e = sqrt(e/len(temp))
print ("Error medio cuadrático %f" % e)

grid(True)
ylabel('Temperatura(Grados)/Potencia')
xlabel('Tiempo (min)')
title('Temepratura del horno vs tiempo')
legend(('Temepratura','Calentador','Identificado','low','up'))

img.savefig('datos_originales_ss.png')


# Pid tune
T = 3000.0
L = 700.0
K = 1.2*T/L
Ti = 2*L
Td = 0.5*L

Ki = K*Ts/Ti
Kd = K*Td/Ts
Kp = K

z=tf([1,0],[1],Identified_system.ts)
pid = Kp+Ki/(1-1/z)+Kd*(1-1/z)

closeLoop = feedback(pid*Identified_system.G)

[t,y]=step_response(closeLoop,T=r_[0:800:10])
e = 1-y
[t,m,x]=forced_response(pid,T=r_[0:800:10],U=e)

# Display Oscilations
img = figure(figsize=(6,5))
plot(t,y,t,e,t,m/100.)
#grid(True)
ylabel('Temperatura(Grados)/Mando p.u.')
xlabel('Tiempo (s)')
#xlim((-20,2000))
grid(True)
title('Pid ajustado Kp=%.2f, Ki=%.2f, Kd=%.2f' % (Kp,Ki,Kd))
legend(('Temepratura','Error','Mando'))
img.savefig('pid_adjusted_ss.png')
