#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sippy import * 
from control import * 
from pylab import *

# Tiempo de muestreo
Ts = 10

# Load data from file
f = file("ident_edited.csv","r")
f.readline()
temp = []
u = []
for line in f.readlines():
  data = line.split(",")
  temp.append(float(data[1]))
  u.append(int(data[2]))  
f.close()

minTemp = min(temp)
temp = [x - minTemp for x in temp]

# Identify
Identified_system=system_identification(temp,u,'ARX',tsample=Ts, IC='AIC')
[t,y,x]=forced_response(Identified_system.G,T=r_[0:10*len(u):10],U=u)
print(Identified_system.G)
#print(ss(Identified_system.G))

# Display Data
temp = [x + minTemp for x in temp]
y = [x + minTemp for x in y]
t = [x/60. for x in t]
img = figure(figsize=(6,5))
plot(t,temp,t,u,t,y)
#grid(True)
ylabel('Temperatura(Grados)/Potencia')
xlabel('Tiempo (min)')
title('Temepratura del horno vs tiempo')
legend(('Temepratura','Calentador','Identificado'))

img.savefig('datos_originales.png')

# Oscilations for Ziegler-Nichols
z=tf([1,0],[1],Identified_system.ts)
Kp = 14.28
Ki = 0
Kd = 0
pid = Kp+Ki/(1-1/z)+Kd*(1-1/z)

closeLoop = feedback(pid*Identified_system.G)

[t,y]=step_response(closeLoop,T=r_[0:10*len(u):10])


# Display Oscilations
img = figure(figsize=(6,5))
plot(t,y)
grid(True)
ylabel('Temperatura(Grados)')
xlabel('Tiempo (s)')
title('Controlador proporcional con Kcr=14.28 -> Tcr=340s')

img.savefig('oscilations.png')

# Pid tune
Kcr = 14.28 
Tcr=340
K = 0.5*Kcr
Ti = 0.5*Tcr
Td = 0.125*Tcr

Ki = K*Ts/Ti
Kd = K*Td/Ts
Kp = K-Ki/2

pid = Kp+Ki/(1-1/z)+Kd*(1-1/z)

closeLoop = feedback(pid*Identified_system.G)

[t,y]=step_response(closeLoop,T=r_[0:2000:10])
e = 1-y
[t,m,x]=forced_response(pid,T=r_[0:2000:10],U=e)

# Display Oscilations
img = figure(figsize=(6,5))
plot(t,y,t,e,t,m/100.)
#grid(True)
ylabel('Temperatura(Grados)/Mando p.u.')
xlabel('Tiempo (s)')
xlim((-20,2000))
grid(True)
title('Pid ajustado Kp=%.2f, Ki=%.2f, Kd=%.2f' % (Kp,Ki,Kd))
legend(('Temepratura','Error','Mando'))
img.savefig('pid_adjusted.png')
