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

# Ring
ringOn  = 3

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

def get_temp(req, resp):
    values = {"temperature": controller.temperature,
              "regulator": controller.pidParams.output,
              "error":(controller.pidParams.setpoint-controller.pidParams.input),
              "inAuto":controller.pid.inAuto,
              "lowerPower":controller.lowerResistor,
              "upperPower":controller.upperResistor}
    yield from picoweb.jsonify(resp, values)

def set_auto(req, resp):    
    req.parse_qs()
    temp = float(req.form['temp'])
    controller.setAuto(temp)
    yield from picoweb.jsonify(resp, {'help':'set_auto?temp=100'})
    
def set_manual(req, resp):    
    req.parse_qs()
    print(req.form)
    lower = int(req.form['lower'])
    upper = int(req.form['upper'])
    controller.setManual(upper, lower)
    yield from picoweb.jsonify(resp, {'help':'set_manual?lower=50&upper=50'})
    
    
def set_rings(req, resp):    
    req.parse_qs()
    ringOn = int(req.form['rings'])
    yield from picoweb.jsonify(resp, {'help':'set_rings?rings=3'})
    
async def ringing():    
    global ringOn, dOuts
    while(1):
        if ringOn > 0:
            dOuts.digitalWrite(buzzer,1)
            await asyncio.sleep(0.5)
            dOuts.digitalWrite(buzzer,0)
            ringOn -= 1
            await asyncio.sleep(0.5)
        else:
            await asyncio.sleep(1)

async def updateDisplay():    
    global temp, tempSensor, display
    while(1):
        display.updateTemperature(controller.temperature)
        await asyncio.sleep(10)
    
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
    #loop.create_task(ringing())
    loop.create_task(updateDisplay())
    loop.create_task(runController())

    ROUTES = [
        # You can specify exact URI string matches...
        ("/", lambda req, resp: (yield from app.sendfile(resp, "horno.html"))),
        ("/w3.css", lambda req, resp: (yield from app.sendfile(resp, "w3.css"))),
        ("/webrepl.html", lambda req, resp: (yield from app.sendfile(resp, "webrepl.html"))),
        ("/FileSaver.js", lambda req, resp: (yield from app.sendfile(resp, "FileSaver.js"))),
        ("/term.js", lambda req, resp: (yield from app.sendfile(resp, "term.js"))),
        ('/set_auto', set_auto),
        ('/set_manual', set_manual),
        ('/get_temp', get_temp),
        ('/set_rings', set_rings),
        ('/webrepl', lambda req, resp: (yield from app.sendfile(resp, "webrepl.html"))),
    ]
    app = picoweb.WebApp(name, ROUTES)

    # debug values:
    # -1 disable all logging
    # 0 (False) normal logging: requests and errors
    # 1 (True) debug logging
    # 2 extra debug logging
    app.run(host="0.0.0.0", port=80, debug=1)

