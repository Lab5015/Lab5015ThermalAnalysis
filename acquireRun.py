from datetime import datetime
import sys
import time
import logging
from optparse import OptionParser

sys.path.append("/home/cmsdaq/Lab5015Utils/")
from Lab5015_utils import read_arduino_temp
from Lab5015_utils import Keithley2450
from Lab5015_utils import sipmTemp
from Lab5015_utils import sipmPower


parser = OptionParser()
parser.add_option("--run")
parser.add_option("--sipmLoad", default = 0.)
parser.add_option("--sipmTemp", default = -999.)

(options,args)=parser.parse_args()


fOut = "/home/cmsdaq/Lab5015ThermalAnalysis/TECScan/run"+str(options.run)+".txt"
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S',filename=fOut,level=logging.INFO)


# turn on SiPM's PS
sipm = None
if options.sipmLoad != 0.:
    sipm = sipmPower(options.sipmLoad)
    sipm.power_on()

# turn on TEC's PS
tec = None
if options.sipmTemp != -999.:
    tec = sipmTemp(options.sipmTemp)
    tec.power_on()
    
init_time = datetime.now()

while True:
    try:
        try:
            temps = read_arduino_temp()
        except ValueError as err:
            print(err)
            print("the returned string is: ",temps)
            time.sleep(1)


        if options.sipmLoad != 0.:
            sipmI = sipm.sipm.meas_I()
            sipmV = sipm.sipm.meas_V()
            sipm.compute_voltage(sipmI, sipmV)


        tecI = 0.
        tecV = 0.
        if options.sipmTemp != -999.:
            (_, tecI, tecV) = tec.TEC.meas_IV()
            tec.compute_voltage(temps[4])

        out = str(tecI)+" "+str(tecV)
        for temp in temps:
            out += " "+temp
        
        logging.info(out)
        sys.stdout.flush()


    except KeyboardInterrupt:
        break
        time.sleep(3)

print("--- powering off both PS")
sipm.power_off()
tec.power_off()
print("bye")
sys.exit(0)
