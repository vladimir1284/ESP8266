# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine, network
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl
# get the interface's IP/netmask/gw/DNS addresses
ap = network.WLAN(network.AP_IF) # create access-point interface
ap.active(True)
# activate the interface
ap.config(essid='Horno', authmode=network.AUTH_OPEN) # set the ESSID of the access point
webrepl.start()
gc.collect()
