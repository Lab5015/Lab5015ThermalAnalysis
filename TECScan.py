from datetime import datetime
import sys
import time
import logging
from optparse import OptionParser

sys.path.append("/home/cmsdaq/Lab5015Utils/")
from Lab5015_utils import read_arduino_temp
from Lab5015_utils import Keithley2450


parser = OptionParser()
parser.add_option("--run")
parser.add_option("--hot", action='store_true')

(options,args)=parser.parse_args()


fOut = "/home/cmsdaq/Lab5015Utils/tectecscan/run"+str(options.run)+".txt"
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S',filename=fOut,level=logging.INFO)

timeout = 480
tensions = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 0.0]
#tensions = [0.0, 0.0, 1.0, 3.0, 5.0, 0.0]
if options.hot:
    tensions = [ -i for i in tensions ]

print(tensions)

mykey = Keithley2450()
mykey.set_V(0)
mykey.set_state(1)

init_time = datetime.now()

for tension in tensions:
    mykey.set_V(tension)

    print("The tension is: ", tension)
    
    while True:
        elapsed_time = datetime.now() - init_time
        temps = read_arduino_temp()

        (_, I, V) = mykey.meas_IV()

        out = str(I)+" "+str(V)
        for temp in temps:
            out += " "+temp
        
        logging.info(out)
        
        if elapsed_time.total_seconds() > timeout:
            init_time = datetime.now()
            break

mykey.set_state(0)
