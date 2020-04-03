import time
import sys
import requests

INTERVAL = 10
url="http://192.168.4.1/get_temp"

def main(argv):
  fname= argv[0]
     
  f=open(fname,"w")
  f.write("Hora,Temperatura\n")

  while(1):
    temp = 0
    for _ in range(INTERVAL):
      r = requests.get(url = url)
      temp += r.json()
      time.sleep(1)
      
    temp = temp/INTERVAL


    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    registerStr = "%s,%.2f\n" % (current_time, temp)
    print(registerStr)
    f.write(registerStr)


if __name__ == "__main__":
  main(sys.argv[1:])
