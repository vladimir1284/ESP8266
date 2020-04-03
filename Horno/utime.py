import time

factor = 1000

def ticks_ms():
    return int(round(time.time() * 1000))*factor

def ticks_diff(ticks1, ticks2):
    return ticks1 - ticks2
