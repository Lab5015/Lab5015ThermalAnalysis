from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from time import sleep, strftime, time
from datetime import datetime
import sys
from optparse import OptionParser

sys.path.append("/home/cmsdaq/Lab5015Utils/")
from Lab5015_utils import read_arduino_temp


parser = OptionParser()
parser.add_option("--inFile","--inFile")
(options,args)=parser.parse_args()


plt.ion()
mytime = []
mytemps = defaultdict(list)

labels = []

labels.append("LYSO")
labels.append("dissipator side")
labels.append("Cold Plate")
labels.append("hot TEC side")
labels.append("SiPMS")
labels.append("Humidity")
labels.append("Air Temperature")


def graph():

    plt.clf()

    plt.grid(b=True,which='major')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
    
    axes = plt.gca()
    axes.set_ylim([0.,40.])

    for sensor,data in mytemps.items():
        plt.plot(mytime,data,label=labels[int(sensor)])
    plt.legend()

    plt.gcf().autofmt_xdate()
    plt.gcf().autofmt_xdate()        
    plt.show()

    

if options.inFile == "live":
    while True:
    
        temps = read_arduino_temp()
        out = ""
        for position in range(len(temps)):
            mytemps[position].append(float(temps[position]))
            out += str(temps[position])+" "

        time = datetime.now()
        mytime.append(time)

        print(time.strftime("%Y-%m-%d %H:%M:%S")+" "+out )
            
        graph()
        plt.pause(1)



else:
    with open(str(options.inFile), 'r') as fin:
        for line in fin.readlines() [-20000:]:
            readings = line.strip().split()
            nreadings = len(readings)
            mytime.append(datetime.strptime(readings[0]+" "+readings[1], "%Y-%m-%d %H:%M:%S")) 
            for position in range(4,nreadings):
                #if isinstance(position, float):
                mytemps[position-4].append(float(readings[position]))
    
    while True:
        with open(str(options.inFile), 'r') as fin:
            for line in fin.readlines() [-1:]:
                readings = line.strip().split()
                nreadings = len(readings)
        
                mytime.append(datetime.strptime(readings[0]+" "+readings[1], "%Y-%m-%d %H:%M:%S"))
                for position in range(4,nreadings):
                    mytemps[position-4].append(float(readings[position]))


        graph()
        plt.pause(1)

