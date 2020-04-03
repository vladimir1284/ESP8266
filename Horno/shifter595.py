class Shifter:  
  def __init__(self, ser, clk):
    # ser - data pin, clk - srclk, rclk pin
    self.ser = ser 
    self.clk = clk
    
  def sendData(self, data):
    for bit in data:
      self.clk.off()
      self.ser.value(bit)
      self.clk.on()
    self.clk.off()
    self.clk.on()

def main():
  from machine import Pin
  ser = Pin(2, Pin.OUT)                                                                                                                                 
  clk = Pin(0, Pin.OUT)
  s = Shifter(ser,clk)
  s.sendData([0,0,0])
