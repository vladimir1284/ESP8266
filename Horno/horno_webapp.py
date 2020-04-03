#
# This is a picoweb example showing a centralized web page route
# specification (classical Django style).
#
import picoweb
import uasyncio as asyncio
from max6675 import MAX6675
from machine import Pin
from display import Display

# Sensor
so = Pin(12, Pin.IN)
sck = Pin(14, Pin.OUT)
cs = Pin(16, Pin.OUT)
tempSensor = MAX6675(sck, cs , so)
temp = 0

display=Display()

def get_temp(req, resp):
    yield from picoweb.jsonify(resp, temp)


async def updateDisplay():    
    global temp, tempSensor, display
    while(1):
        temp=tempSensor.read()
        display.updateTemperature(temp)
        await asyncio.sleep(10)
    

import ulogging as logging
#logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

def main(name):
    # loop = asyncio.get_event_loop()
    # loop.create_task(updateDisplay())

    ROUTES = [
        # You can specify exact URI string matches...
        ("/", lambda req, resp: (yield from app.sendfile(resp, "horno.html"))),
        ("/w3.css", lambda req, resp: (yield from app.sendfile(resp, "w3.css"))),
        ("/webrepl.html", lambda req, resp: (yield from app.sendfile(resp, "webrepl.html"))),
        ("/FileSaver.js", lambda req, resp: (yield from app.sendfile(resp, "FileSaver.js"))),
        ("/term.js", lambda req, resp: (yield from app.sendfile(resp, "term.js"))),
        ('/get_temp', get_temp),
        ('/webrepl', lambda req, resp: (yield from app.sendfile(resp, "webrepl.html"))),
    ]
    app = picoweb.WebApp(name, ROUTES)

    # debug values:
    # -1 disable all logging
    # 0 (False) normal logging: requests and errors
    # 1 (True) debug logging
    # 2 extra debug logging
    app.run(host="0.0.0.0", port=80, debug=1)

