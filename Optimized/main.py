#biblioteki zew
import schedule
import time
from datetime import datetime
import multiprocessing

#import plikow wew
import threadAccelerationController as ta
import threadAnomalyDetectionController as tad
import threadCountAnomaliesController as tca
import threadProcessController as tp
import threadPreProcessingController as tpp
import globals

manager = multiprocessing.Manager()
d = manager.dict()
d["Process"] = False
d["Acceleration"] = False
d["PreProcessing"] = False
d["AnomalyDetection"] = False
d["RoundAnomalies"] = False
d["CountAnomalies"] = False
d["allFilesProcessedFlag"] = False
d["end"] = False

logsPath = "Log" + str(datetime.now()) + ".txt"

def startLog():
    global logsPath
    logfile = open(logsPath, "w+")
    logfile.write("Program main.py started at: " + str(datetime.now()) + "\n")
    logfile.close()
    print("Program started, " + str(datetime.now()))

def startThreads():
    if not d["Process"] and not d["allFilesProcessedFlag"]:
        thread1 = multiprocessing.Process(target=tp.startThread, args=(d,), name="Process")
        thread1.daemon = True
        thread1.start()
        d["Process"] = True
    if not d["Acceleration"]:
        thread2 = multiprocessing.Process(target=ta.startThread, args=(d,), name="Acceleration")
        thread2.daemon = True
        thread2.start()
        d["Acceleration"] = True
    if not d["PreProcessing"]:
        thread3 = multiprocessing.Process(target=tpp.startThread, args=(d,), name="PreProcessing")
        thread3.daemon = True
        thread3.start()
        d["PreProcessing"] = True
    if not d["AnomalyDetection"]:
        thread3 = multiprocessing.Process(target=tad.startThread, args=(d,), name="AnomalyDetection")
        thread3.daemon = True
        thread3.start()
        d["AnomalyDetection"] = True
    if not d["CountAnomalies"] and d["allFilesProcessedFlag"]:
        thread5 = multiprocessing.Process(target=tca.startThread, args=(d,), name="CountAnomalies")
        thread5.daemon = True
        thread5.start()
        d["CountAnomalies"] = True

def addLog(message):
    global logsPath
    string = str(datetime.now()) + " " + message
    print(string)
    logfile = open(logsPath, "a+")
    logfile.write(string + "\n")
    logfile.close()


def mainController():
    startLog()
    startThreads()
    globals.initialize()
    schedule.every(1).minutes.do(startThreads)
    while not d["end"]:
        schedule.run_pending()
        time.sleep(30)
    addLog("This is end")

if __name__== "__main__":
    mainController()