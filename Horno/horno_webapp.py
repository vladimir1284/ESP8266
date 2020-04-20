#
# This is a picoweb example showing a centralized web page route
# specification (classical Django style).
#
import picoweb
import uasyncio as asyncio
from max6675 import MAX6675
from machine import Pin
from display import Display
from shifter595 import DigitalOutputs595
from horno_controller import Horno
import utime

# Timer
ringOn  = 0
timerFinish = 0 # ms

# Digital Outputs
buzzer = 2
dOuts = DigitalOutputs595(2,0,13,3)

# Sensor
so = Pin(12, Pin.IN)
sck = Pin(14, Pin.OUT)
cs = Pin(16, Pin.OUT)
tempSensor = MAX6675(sck, cs , so)

# Oven controler
controller = Horno(tempSensor, dOuts)

# Display
display=Display()


values = {"temperature": controller.temperature,
          "regulator": controller.pidParams.output,
          "error":(controller.pidParams.setpoint-controller.pidParams.input),
          "inAuto":controller.pid.inAuto,
          "ready":controller.ready,
          "timer":(timerFinish - utime.ticks_ms()),
          "on":controller.on,
          "lowerPower":controller.lowerResistor,
          "upperPower":controller.upperResistor}

def get_values(req, resp): 
    global timerFinish, values
    values["temperature"] = controller.temperature
    values["regulator"] = controller.pidParams.output
    values["error"] = controller.pidParams.setpoint-controller.pidParams.input
    values["inAuto"] = controller.pid.inAuto
    values["timer"] = timerFinish - utime.ticks_ms()
    #values["ready"] = controller.ready
    values["on"] = controller.on
    values["lowerPower"] = controller.lowerResistor
    values["upperPower"] = controller.upperResistor
    yield from picoweb.jsonify(resp, values)

def set_auto(req, resp):    
    req.parse_qs()
    controller.setAuto(float(req.form['temp']))
    yield from picoweb.jsonify(resp, {'help':'set_auto?temp=100'})
    
def set_manual(req, resp):    
    req.parse_qs()
    controller.setManual(int(req.form['upper']), int(req.form['lower']))
    yield from picoweb.jsonify(resp, {'help':'set_manual?lower=50&upper=50'})
    
def turnOFF(req, resp):    
    global timerFinish
    controller.turnOFF()
    timerFinish = 0
    display.updateTimer(0)
    yield from picoweb.jsonify(resp, {'help':'turn_off'})
    
def set_timer(req, resp):  
    global timerFinish  
    req.parse_qs()
    timerFinish = utime.ticks_ms()+60000*int(req.form['minutes'])
    yield from picoweb.jsonify(resp, {'help':'set_timer?minutes=20'})
    
async def timer():    
    global ringOn, timerFinish
    while(1):
        if ringOn > 0:
            dOuts.digitalWrite(buzzer,1)
            await asyncio.sleep(0.5)
            dOuts.digitalWrite(buzzer,0)
            ringOn -= 1
            await asyncio.sleep(0.5)
        else:
            if (timerFinish != 0):
                if (utime.ticks_ms() > timerFinish): # Timer finished
                    timerFinish = 0
                    ringOn = 3
                    controller.turnOFF()
            await asyncio.sleep(1)

async def updateDisplay():      
    global ringOn, timerFinish
    while(1):
        # Check for ready state
        if (values["ready"] != controller.ready):
            values["ready"] = controller.ready
            if (values["ready"]):
                # Two bips for the user
                ringOn = 2
            
        # Temperature  
        display.updateTemperature(controller.temperature)
        
        # Timer
        if(timerFinish != 0):
            display.updateTimer((timerFinish - utime.ticks_ms()) / 60000)
        await asyncio.sleep(1)
    
async def runController():    
    global controller
    while(1):
        controller.run()
        await asyncio.sleep(0.1)

import ulogging as logging
#logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

def main(name):
    loop = asyncio.get_event_loop()
    loop.create_task(timer())
    loop.create_task(updateDisplay())
    loop.create_task(runController())

    ROUTES = [
        # You can specify exact URI string matches...
        ("/", lambda req, resp: (yield from app.sendfile(resp, "horno.html"))),
        ("/horno.js", lambda req, resp: (yield from app.sendfile(resp, "horno.js"))),
        ("/gauge.min.js", lambda req, resp: (yield from app.sendfile(resp, "gauge.min.js"))),
        ("/input-knobs.js", lambda req, resp: (yield from app.sendfile(resp, "input-knobs.js"))),
        ("/w3.css", lambda req, resp: (yield from app.sendfile(resp, "w3.css"))),
        ("/webrepl.html", lambda req, resp: (yield from app.sendfile(resp, "webrepl.html"))),
        ("/FileSaver.js", lambda req, resp: (yield from app.sendfile(resp, "FileSaver.js"))),
        ("/term.js", lambda req, resp: (yield from app.sendfile(resp, "term.js"))),
        ('/set_auto', set_auto),
        ('/set_manual', set_manual),
        ('/get_values', get_values),
        ('/turn_off', turnOFF),
        ('/set_timer', set_timer),
        ('/webrepl', lambda req, resp: (yield from app.sendfile(resp, "webrepl.html"))),
    ]
    app = picoweb.WebApp(name, ROUTES)

    # debug values:
    # -1 disable all logging
    # 0 (False) normal logging: requests and errors
    # 1 (True) debug logging
    # 2 extra debug logging
    app.run(host="0.0.0.0", port=80, debug=-1)

