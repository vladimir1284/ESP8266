from pylab import *

class Model:
  def __init__(self):
    self.Xi = 0*ones(71)
    self.Yi = [0,0,0,0,0]
    
  def evaluate(self, x):
    y = (0.01824*self.Xi[70]+ 0.3369*self.Yi[0] + 0.2516*self.Yi[1]
        + 0.092795*self.Yi[2] + 0.1174*self.Yi[3] + 0.1927*self.Yi[4])
    for i in range(4, 0, -1):
      self.Yi[i] = self.Yi[i - 1]
    for i in range(70, 0, -1):      
      self.Xi[i] = self.Xi[i - 1]
    self.Xi[0] = x
    self.Yi[0] = y
    return y

def main():
  # Check step response
  
  # Load data from file
  f = file("step-30.csv","r")
  f.readline()
  temp = []
  u = []
  for line in f.readlines():
    data = line.split(",")
    temp.append(float(data[1]))
    u.append(float(data[6]))  
  f.close()
    
  minTemp = min(temp)
  temp = [x - minTemp for x in temp]
  
  # Evaluate the model
  horno = Model()
  y = zeros(len(u))
  for i,x in enumerate(u):
    y[i] = horno.evaluate(x)
  
  #print y[0:20]
  
  # Plot results
  temp = [x + minTemp for x in temp]
  y = [x + minTemp for x in y]
  t = r_[0:10*len(u):10]/60.
  
  img = figure(figsize=(6,5)) # figsize=(4,8)
  plot(t,temp,t,u,t,y)
  grid(True)
  ylabel('Temperatura(Grados)/Potencia')
  xlabel('Tiempo (min)')
  title('Temepratura del horno vs tiempo')
  legend(('Temepratura','Calentador','Identificado'))

  img.savefig('test_model_ss.png')
  
if __name__ == "__main__":
	main()
