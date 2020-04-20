import time 
from PID import PID, PIDParams
from model_ss import Model
from pylab import *

# Kcr = 11.28
# Tcr = 400
Ts = 10

# K = 0.5*Kcr
# Ti = 0.5*Tcr
# Td = 0.125*Tcr

# Ki = K*Ts/Ti
# Kd = K*Td/Ts
# Kp = K-Ki/2

setPoint = 10

model = Model()
pidParams = PIDParams(input = 0, output = 0, setpoint = setPoint)
pid = PID(params = pidParams, kP = 0, kI = 0, kD = 0, direction = PID.DIRECT, debugEnabled = True)
pid.setMode(PID.AUTOMATIC)
pid.sampleTime = 10000 # ms
pid.setTunings(2,0.0008,0)#0.004,100)
#pid.setTunings(Kp,Ki,Kd)
pid.setOutputLimits(0, 100)
pid.debugEnabled = False

print(pid.sampleTime)
print(pid.outputMin)
print(pid.outputMax)


M=[]
Y=[]
E=[]
simulationTime = 10000
for i in range(0, simulationTime/Ts):
    res = pid.compute()
    M.append(pidParams.output)
    time.sleep(0.01)
    y = model.evaluate(pidParams.output)
    E.append(setPoint-y)
    pidParams.input = y
    Y.append(y)

t = r_[0:simulationTime:Ts]/60.0

img = figure(figsize=(6,5)) 
plot(t,Y,t,E,t,M)
grid(True)
ylabel('Temperatura(Grados)')
xlabel('Tiempo (min)')
title('Pid ajustado Kp=%.2f, Ki=%.2f, Kd=%.2f' % (pid.kP,pid.kI,pid.kD))
legend(('Temperatura','Error','Mando'))
img.savefig('test_pid_ss.png')
