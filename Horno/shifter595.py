from machine import Pin

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

class DigitalOutputs595:
    def __init__(self, ser_pin, clk_pin, size):
      self.data = []
      for _ in range(size):
        self.data.append(0)
      ser = Pin(ser_pin, Pin.OUT)                                                                                                                                 
      clk = Pin(clk_pin, Pin.OUT)
      self.shifter = Shifter(ser,clk)
      self.shifter.sendData(self.data)
      
    def digitalWrite(self, address, value):
      self.data[address] = value
      self.shifter.sendData(self.data)
      
    def getValue(self, address):
      return self.data[address]
