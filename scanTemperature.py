import sys
import time

sys.path.append("/home/cmsdaq/Lab5015Utils/")
from Lab5015_utils import SMChiller

SMC = SMChiller()
tempList = [35,30,25,20,15,10]

for temp in tempList:
    print("set temp to: ",temp)
    SMC.write_set_temp(temp)
    time.sleep(900)
SMC.set_state(0)
