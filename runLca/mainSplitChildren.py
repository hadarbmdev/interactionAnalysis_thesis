from py.runLca.utils import runMplus, analyzeOutput, prepareInputFileWithName, rollBehaviors, deleteInputAndOutpusFiles, children_behaviors
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
import csv
# REPLACE GELEM!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

numberOfMachines = 1
machineNumber = 1


def main():

    error = ""

    file = open("C:\\TEMP\\mplus\\errors.txt", "w+")
    file. truncate(0)
    file. close()
    filePrefix = "_children"
    permCounter = 0
    for i in range(3, 6):
        perms = rollBehaviors(i, children_behaviors)

        #permCounter = permCounter + len(perms)
        # writePermsToFile('permFile'+str(i)+'.txt', perms)
        writePermsToFile('permFileChildren.txt', perms)
    with open("C:\\TEMP\\mplus\\mplusFilesLog"+filePrefix+".csv", "a", newline='') as text_file:
        writer = csv.writer(text_file)
        writer.writerow(["iteration", "file name", "vars",
                         "# vars", "c1", "c2", "c3", "allVarsMeans"])

    with open("C:\\TEMP\\mplus\\means_of_vars"+filePrefix+".csv", "a", newline='') as text_file:
        writer = csv.writer(text_file)
        writer.writerow(["iteration", "vars",
                         "Mean of Var:", "c1", "c2", "c3"])

    text_file.close()

    machineRange = preparePermFileRanges('permFileChildren.txt', machineNumber)
    sMin = 3
    sAvg = 5
    sMax = 9
    t1 = dt.now()
    for i in machineRange:
        vars = extractVarsFromPermFile('permFileChildren.txt', i)
        splitVars = vars.replace("'", "").replace(")", "").replace(
            "(", "").replace(" ", "").split(',')
        print(vars)

        runMplusOnPermutaion(vars, i, sMin, sAvg, sMax, splitVars, filePrefix)


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


def runMplusOnPermutaion(vars, c, sMin, sAvg, sMax, splitVars, filePrefix):
    t2 = datetime.now()
    print(t2.strftime("%H:%M:%S") + ": "+str(c) +
          '+ :running mplus on vars: '+str(vars))
    try:
        prepareInputFileWithName(
            vars, c, "C:\\TEMP\\mplus\\current_template_children.inp", "_children")
        runMplus(vars, c, "_children")
        analyzeOutput(c, len(vars*2), vars, "_children",
                      sMin, sAvg, sMax, splitVars)
        deleteInputAndOutpusFiles(c, filePrefix)
        print('done iteration '+str(c))
    except Exception as e:
        print("FAILED! failed vars: "+str(vars)+"\n"+"error:"+"\n"+str(e))
        text_file = open("C:\\TEMP\\mplus\\errors.txt", "a")
        text_file.write(
            "failed vars: "+str(vars)+"\n"+"error:"+"\n"+str(e) + "\n")
        text_file.write(e.stack)
        text_file.write("\n")
        text_file.close()
    finally:
        t3 = datetime.now()
        took = (t3 - t2)/12
        print('it took :' + str(took))


main()
