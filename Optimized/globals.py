#biblioteki zew
from configparser import ConfigParser

contamination=0
maximumBreakValue = 0
errorValue = 0
minValue = 0

import main as m
import sys
def initialize():
    global contamination, maximumBreakValue, errorValue, minValue

    parser = ConfigParser()
    parser.read('config.ini')
    try:
        contamination = parser.getfloat('AnomalyConfiguration', 'contamination')
        maximumBreakValue = parser.getfloat('AnomalyConfiguration', 'maximumBreakValue')
        errorValue = parser.getfloat('AnomalyConfiguration', 'errorValue')
        minValue = parser.getfloat('AnomalyConfiguration', 'minValue')
        return True
    except Exception as e:
        m.addLog("Incorrect value in config.ini, exception: " + str(e))
        sys.exit()




