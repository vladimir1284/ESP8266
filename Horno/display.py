from machine import Pin, I2C
import ssd1306

class Display:
  def __init__(self):    
    self.lastTemp = 0
    self.lastTime = 0
    self.dotsState = 0
    
    # Oled
    i2c = I2C(-1, scl=Pin(5), sda=Pin(4))
    oled_width = 128
    oled_height = 32
    self.oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

    # Draw oven template
    x0 = 97
    self.oled.framebuf.rect(x0,0,31,32,1)
    self.oled.framebuf.line(x0,23,x0+31,23,1)
    self.oled.framebuf.line(x0,8,x0+31,8,1)    

    # Draw thermomemter template
    x0 = 86
    self.fillCircle(x0,27,4,1)
    self.drawCircle(x0,2,2,1)
    self.oled.framebuf.line(x0+2,23,x0+2,2,1)
    self.oled.framebuf.line(x0-2,23,x0-2,2,1)
    self.oled.framebuf.fill_rect(x0-1,2,3,22,0)
    
    # Draw timer template
    x0 = 63
    self.drawCircle(x0,12,8,1)
    self.drawCircle(x0,12,9,1)
    self.oled.framebuf.line(x0,12,x0,9,1)
    self.oled.framebuf.line(x0,12,x0+4,15,1)
    self.oled.framebuf.line(x0-9,2,x0-4,0,1)  
    self.oled.framebuf.line(x0-9,3,x0-4,1,1)
    self.oled.framebuf.line(x0+9,2,x0+4,0,1)  
    self.oled.framebuf.line(x0+9,3,x0+4,1,1)
    
    # Draw stove template
    x0 = 6
    self.drawCircle(x0,25,6,1)
    self.drawCircle(x0+18,25,6,1)
    self.drawCircle(x0+18,6,6,1)    
    
    # Finish template
    self.oled.show()

  def updateTimer(self, delay):
    delay = int(delay)
    if (delay != self.lastTime):
      self.lastTime = delay
      # Time in minutes to HH:MM
      HH = delay/60
      MM = delay%60
      # Update number
      x0 = 50
      self.oled.framebuf.fill_rect(x0,24,27,8,0)
      self.oled.text("%1i" % HH,x0,24)
      self.oled.text("%02i" % MM,x0+11,24)  
    if (delay != 0):  
      self.alternateDots()

  def alternateDots(self):
    x0 = 50
    self.dotsState = not(self.dotsState)
    self.oled.pixel(x0+9, 26, self.dotsState)
    self.oled.pixel(x0+9, 29, self.dotsState)
    self.oled.show() 

  def updateTemperature(self, temp):
    temp = int(temp)
    if (temp != self.lastTemp):
      lastTemp = temp
      # Update number
      x0 = 100
      self.oled.framebuf.fill_rect(x0,12,24,8,0)
      self.oled.text("%3i" % temp,x0,12)
      # Update icon
      x0 = 85
      self.oled.framebuf.fill_rect(x0,2,3,22,0)
      h = int((temp-30)*0.0594)
      self.oled.framebuf.fill_rect(x0,24-h,3,h,1)
      self.oled.show() 

  # Draw a filled circle    
  def fillCircle(self, x0, y0, r, color):
      f = 1 - r
      ddF_x = 1
      ddF_y = -2 * r
      x = 0
      y = r
      self.oled.framebuf.line(x0  , y0+r, x0  , y0-r, color)
      self.oled.framebuf.line(x0+r, y0  , x0-r, y0  , color)
      while (x<y):
          if (f >= 0):
              y -= 1
              ddF_y += 2
              f += ddF_y
              
          x += 1
          ddF_x += 2
          f += ddF_x
          self.oled.framebuf.line(x0 + x, y0 + y, x0 - x, y0 + y, color)
          self.oled.framebuf.line(x0 + x, y0 - y, x0 - x, y0 - y, color)
          self.oled.framebuf.line(x0 + y, y0 + x, x0 - y, y0 + x, color)
          self.oled.framebuf.line(x0 + y, y0 - x, x0 - y, y0 - x, color)

  # Draw a circle outline
  def drawCircle(self, x0, y0, r, color):
      f = 1 - r
      ddF_x = 1
      ddF_y = -2 * r
      x = 0
      y = r
      self.oled.pixel(x0  , y0+r, color)
      self.oled.pixel(x0  , y0-r, color)
      self.oled.pixel(x0+r, y0  , color)
      self.oled.pixel(x0-r, y0  , color)

      while (x<y):
          if (f >= 0):
              y -= 1
              ddF_y += 2
              f += ddF_y
              
          x += 1
          ddF_x += 2
          f += ddF_x

          self.oled.pixel(x0 + x, y0 + y, color)
          self.oled.pixel(x0 - x, y0 + y, color)
          self.oled.pixel(x0 + x, y0 - y, color)
          self.oled.pixel(x0 - x, y0 - y, color)
          self.oled.pixel(x0 + y, y0 + x, color)
          self.oled.pixel(x0 - y, y0 + x, color)
          self.oled.pixel(x0 + y, y0 - x, color)
          self.oled.pixel(x0 - y, y0 - x, color)
