from py.runLca.utils import runMplusWithSaveFile, analyzeOutput, prepareInputFile, rollBehaviors, deleteInputAndOutpusFiles, getSubjectsArrNames, subjects, analyzeOutputToGetMothersOfEachSubjectLCAGroup, prepareInputFileWithName, NoEmptyObservations, analyzeOutputToGetMothersOfEachSubjectLCAGroup
import logging
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
import pandas as pd
# REPLACE GELEM!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

numberOfMachines = 10
machineNumber = 10


def main():

    error = ""

    file = open("C:\\TEMP\\mplus\\errors.txt", "w+")
    file. truncate(0)
    file. close()
    filePrefix = "_children"

    # getSubjectsArrNames()
    gelem = pd.read_csv('C:\\TEMP\\mplus\\gelemChildrenWithW5data.csv')
    lcaGroups = pd.read_csv(
        'C:\\TEMP\\mplus\\childrenAboveThreshold.csv', na_filter=False)
    for index, row in lcaGroups.iterrows():
        # print(row)
        iterName = 'lca_'+str(row['iteration'])
        lcaVars = row['vars']
        splitVars = lcaVars.replace("'", "").replace(")", "").replace(
            "(", "").replace(" ", "").split(',')
        if (NoEmptyObservations(gelem, splitVars)):
            runMplusOnPermutaion(
                lcaVars, row['iteration'], filePrefix, splitVars)
            break

    # with open("C:\\TEMP\\mplus\\motherLCAfilteredMinGroup15andUp.csv", "r", newline='') as text_file:
    #     writer = csv.writer(text_file)
    #     writer.writerow(["iteration", "file name", "vars",
    #                      "# vars", "c1", "c2", "c3"])
    # text_file.close()

    # machineRange = preparePermFileRanges('permFile.txt', machineNumber)

    # t1 = dt.now()
    # for i in machineRange:
    #     vars = extractVarsFromPermFile('permFile.txt', i)
    #     print(vars)
    #     runMplusOnPermutaion(vars, i)


def runMplusOnPermutaion(vars, c, filePrefix, splitVars):
    t2 = datetime.now()
    print(t2.strftime("%H:%M:%S") + " iteration: #"+str(c) +
          ': running mplus on vars: '+str(vars))
    try:
        prepareInputFileWithName(
            vars, c, "C:\\TEMP\\mplus\\current_template"+filePrefix+".inp", "_children")
        runMplusWithSaveFile(vars, c, filePrefix)
        # analyzeOutputToGetMothersOfEachSubjectLCAGroup(c, len(vars*2), vars)
        analyzeOutputToGetMothersOfEachSubjectLCAGroup(
            c, len(vars*2), vars, filePrefix, splitVars)
        deleteInputAndOutpusFiles(c, filePrefix)
        print('done iteration '+str(c))
    except Exception as e:
        # print("FAILED! failed vars: "+str(vars)+"\n"+"error:"+"\n"+str(e))
        logging.exception("FAILED! failed vars: "+str(vars)+"\n"+"error:")
        text_file = open("C:\\TEMP\\mplus\\errors.txt", "a")
        text_file.write(
            "failed vars: "+str(vars)+"\n"+"error:"+"\n"+str(e))
        text_file.close()
    finally:
        t3 = datetime.now()
        took = (t3 - t2)/12
        print('it took :' + str(took))


main()
