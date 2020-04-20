import time
import sys
import requests

INTERVAL = 10
url="http://192.168.4.1/get_values"

def main(argv):
  fname= argv[0]
     
  f=open(fname,"w")
  f.write("datetime,temperature,regulator,error,inAuto,ready,lowerPower,upperPower\n")

  while(1):
    r = requests.get(url = url)
    data = r.json()

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    registerStr = "%s,%.2f,%.2f,%.2f,%i,%i,%i,%i\n" % (current_time, 
                                                       data["temperature"], 
                                                       data["regulator"], 
                                                       data["error"], 
                                                       data["inAuto"], 
                                                       data["ready"], 
                                                       data["lowerPower"], 
                                                       data["upperPower"])
    print(registerStr)
    f.write(registerStr)
    time.sleep(INTERVAL)


if __name__ == "__main__":
  main(sys.argv[1:])
