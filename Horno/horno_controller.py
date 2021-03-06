from PID import PIDParams, PID
import utime


class Horno:
  # Constants
  upperR     = 1     # Digital output index
  lowerR     = 0     # Digital output index
  Ts         = 10000 # Sampling period (ms)
  Tread      = 1000  # Temperature reading interval (ms)
  Tresist    = 100   # Resistance managment interval (ms)
  windowSize = 10    # Number of samples for the average filter
  thress     = 44    # After this output value the lower resistor 
                     # is totaly on and the upper resistor starts
  H1         = 30    # Degrees below setpoint to enable PID
  HoldTime   = 150000# Milliseconds after first heating to turn PID on
  
  # Constructor
  def __init__(self, sensor, dOuts):
    # PID
    self.pidParams = PIDParams(input = 0, output = 0, setpoint = 0)
    self.pid = PID(params = self.pidParams, kP = 0, kI = 0, kD = 0, 
                    direction = PID.DIRECT, debugEnabled = True)
    self.pid.sampleTime = self.Ts # ms
    self.pid.setTunings(2.5,0.005,0)
    self.pid.setOutputLimits(0, 100)
    self.pid.debugEnabled = False
    
    # Resistors
    self.dOuts = dOuts     # DigitalOutputs595 instance
    self.lowerResistor = 0 # Desired power (%)
    self.upperResistor = 0 # Desired power (%)
    self.segmentPWM    = 0 # Current segment of the PWM period
    self.lastPWM       = 0 # Last time of the PWM execution
    
    # Temperature
    self.sensor = sensor                  # Max6675 sensor
    self.temps = [30.0] * self.windowSize # Temperature sliding window
    self.tempsHead = 0                    # Pointer to the head of the sliding window
    self.temperature = 30.0               # Average temperature
    self.lastRead = 0
    self.t = 0
    
    # Status
    self.on = False
    self.ready = False
    self.starting = 0
    self.turnOFF()
    
    
  def run(self):    
    now = utime.ticks_ms()
        
    # Handle temperature and PID
    timeChange = utime.ticks_diff(now, self.lastRead)
    if (timeChange > self.Tread):
      self.tempFilter()
      self.pidParams.input = self.temperature  
      self.pid.compute()
      self.lastRead = now
    
    if (self.on):      
      # Verify ready
      if (self.pid.inAuto):
        if (self.temperature > self.pidParams.setpoint):
          self.ready = True
      
      # Handle resistors
      timeChange = utime.ticks_diff(now, self.lastPWM)
      if (timeChange > self.Tresist):
        self.handleResistors()
        self.lastPWM = now

  def handleResistors(self):
    if (self.pid.inAuto):
      # First Heating zone    
      if ((self.temperature < self.pidParams.setpoint-self.H1) and (self.starting == 0)):
          self.lowerResistor = 100
          self.upperResistor = 100
      else:
          now = utime.ticks_ms()
          if (self.starting == 0):
            self.starting = now
          if (now - self.starting > self.HoldTime):
            # PID activate
            self.lowerResistor = self.pidParams.output
            self.upperResistor = self.pidParams.output
          else:
            self.lowerResistor = 0
            self.upperResistor = 0
            self.pid.iTerm = 0
        
    # PWM upper resistor
    self._pwm(self.upperResistor, self.upperR)
    # PWM lower resistor 
    self._pwm(self.lowerResistor, self.lowerR)
    
    self.segmentPWM = (self.segmentPWM + 1) % 100
    
  def _pwm(self, level, R):
    if (self.segmentPWM < level):
      if (not(self.dOuts.getValue(R))):
        self.dOuts.digitalWrite(R, 1)
    else:
      if (self.dOuts.getValue(R)):
        self.dOuts.digitalWrite(R, 0)      
    
  # Running average filter for temperature readings  
  def tempFilter(self):
    self.t = self.sensor.read()
    self.temperature -= self.temps[self.tempsHead] / self.windowSize
    self.temperature += self.t / self.windowSize
    self.temps[self.tempsHead] = self.t
    self.tempsHead = (self.tempsHead + 1) % self.windowSize
  
  # Start the oven at the desired temperature in automatic mode  
  def setAuto(self, setpoint):
    self.on = True
    self.ready = False
    self.starting = 0
    self.pidParams.setpoint = setpoint
    self.pid.setMode(PID.AUTOMATIC)
  
  # Start the oven at the desired temperature in automatic mode  
  def setManual(self, upperResistor, lowerResistor):
    self.on = True
    self.ready = False
    self.pid.setMode(PID.MANUAL)
    self.lowerResistor = lowerResistor
    self.upperResistor = upperResistor    
  
  # Shuts down the oven  
  def turnOFF(self):
    self.pid.setMode(PID.MANUAL)
    self.lowerResistor = 0
    self.upperResistor = 0
    self.dOuts.digitalWrite(self.lowerR, 0)
    self.dOuts.digitalWrite(self.upperR, 0)
    self.on = False
    self.ready = False
