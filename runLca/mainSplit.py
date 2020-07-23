from py.runLca.utils import runMplus, analyzeOutput, prepareInputFile, rollBehaviors, deleteInputAndOutpusFiles
import pathlib
import sys
import os
import time
from datetime import datetime
from datetime import datetime as dt
from datetime import timedelta
import multiprocessing as mp
from multiprocessing import Process, freeze_support
import threading
import logging
import linecache
# REPLACE GELEM!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

numberOfMachines = 10
machineNumber = 2


def main():

    error = ""

    file = open("C:\\TEMP\\mplus\\errors.txt", "w+")
    file. truncate(0)
    file. close()

    # permCounter = 0
    # for i in range(3, 6):
    #     perms = rollBehaviors(i)

    #     #permCounter = permCounter + len(perms)
    #     # writePermsToFile('permFile'+str(i)+'.txt', perms)
    #     writePermsToFile('permFile.txt', perms)

    machineRange = preparePermFileRanges('permFile.txt', machineNumber)

    t1 = dt.now()
    for i in machineRange:
        vars = extractVarsFromPermFile('permFile.txt', i)
        print(vars)
        runMplusOnPermutaion(vars, i)
        return


def writePermsToFile(permFile, perms):
    with open("C:\\TEMP\\mplus\\perms\\"+permFile, "a") as text_file:
        for item in perms:
            text_file.write(str(item) + "\n")

    text_file.close()


def preparePermFileRanges(permFile, machineNum):
    linesCounter = 0
    with open("C:\\TEMP\\mplus\\perms\\"+permFile, "r") as text_file:
        for line in text_file:
            linesCounter = linesCounter + 1

    text_file.close()
    linesPerMachine = round(linesCounter/numberOfMachines)
    print(linesPerMachine)

    thisMachineTop = (linesPerMachine * machineNum)
    thisMachineBottom = thisMachineTop - linesPerMachine + 1
    machineTuple = (thisMachineBottom, thisMachineTop)
    machineRange = range(thisMachineBottom, thisMachineTop)
    return machineRange


def extractVarsFromPermFile(permFile, lineNumber):
    return linecache.getline("C:\\TEMP\\mplus\\perms\\"+permFile, lineNumber)


def runMplusOnPermutaion(vars, c):
    t2 = datetime.now()
    print(t2.strftime("%H:%M:%S") + ": "+str(c) +
          '+ :running mplus on vars: '+str(vars))
    try:
        prepareInputFile(vars, c)
        runMplus(vars, c)
        analyzeOutput(c, len(vars*2), vars)
        deleteInputAndOutpusFiles(c)
        print('done iteration '+str(c))
    except Exception as e:
        print("FAILED! failed vars: "+str(vars)+"\n"+"error:"+"\n"+str(e))
        text_file = open("C:\\TEMP\\mplus\\errors.txt", "a")
        text_file.write(
            "failed vars: "+str(vars)+"\n"+"error:"+"\n"+str(e))
        text_file.close()
    finally:
        t3 = datetime.now()
        took = (t3 - t2)/12
        print('it took :' + str(took))


main()
