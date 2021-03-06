from datetime import datetime
import sys
import time
import logging
from optparse import OptionParser

sys.path.append("/home/cmsdaq/Lab5015Utils/")
from Lab5015_utils import read_arduino_temp
from Lab5015_utils import Keithley2450
from Lab5015_utils import sipmPower


parser = OptionParser()
parser.add_option("--run")
parser.add_option("--stepTime", default = 480)
parser.add_option("--initialTime", default = 0.)
parser.add_option("--hot", action='store_true')
parser.add_option("--sipmLoad", default = 0.)

(options,args)=parser.parse_args()


fOut = "/home/cmsdaq/Lab5015ThermalAnalysis/TECScan/run"+str(options.run)+".txt"
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S',filename=fOut,level=logging.INFO)


tensions = [0.0, 0.0, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 0.0]
#tensions = [0.0, 1.0, 3.0, 5.0]
#tensions = [0.0,0.0]
if options.hot:
    tensions = [ -i for i in tensions ]
print(tensions)

print("initial timeout: "+str(options.initialTime))
time.sleep(float(options.initialTime))

# turn on SiPM's PS
sipm = None
if float(options.sipmLoad) != 0.:
    sipm = sipmPower(options.sipmLoad)
    sipm.power_on()

# turn on TEC's PS
mykey = Keithley2450()
mykey.set_V(0)
mykey.set_4wire("OFF")
mykey.set_state(1)
state = 0

timeout = float(options.stepTime)
print("timeout per step: ",timeout)

init_time = datetime.now()

for itr,tension in enumerate(tensions):
    try:
        if tension != 0. and state == 0:
            mykey.set_4wire("ON")
            mykey.set_state(1)
            state += 1
        if tension == 0. and state != 0:
            mykey.set_4wire("OFF")
            mykey.set_state(1)
        mykey.set_V(tension)
        print("The tension is: ", tension)
    
        while True:
            elapsed_time = datetime.now() - init_time

            temps = []
            try:
                temps = read_arduino_temp()
            except ValueError as err:
                print(err)
                print("the returned string is: ",temps)
                time.sleep(1)
                continue

            (_, I, V) = mykey.meas_IV()

            out = str(I)+" "+str(V)
            for temp in temps:
                out += " "+temp
        
            logging.info(out)
            sys.stdout.flush()

            if float(options.sipmLoad) != 0.: 
                if itr > 0: # skip the first position
                    sipm.compute_voltage()        
        
            if elapsed_time.total_seconds() > timeout:
                init_time = datetime.now()
                break


    except KeyboardInterrupt:
        break
        time.sleep(3)

print("--- powering off both PS")
if float(options.sipmLoad) != 0.: 
    sipm.power_off()
mykey.set_state(0)
print("bye")
sys.exit(0)
