import math
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import json
from operator import itemgetter
import os
import fileinput
import matplotlib.pyplot as plt
import seaborn as sn
from scipy.stats import spearmanr
from sklearn.cluster import KMeans
from pandas import plotting
from py import global_utils
from py.negPos.utils import BehaviorsEmotions
data = {}

# matrix_input = pd.DataFrame(data)

keysB = ["child neutral affect", "cleanup not requested", "mother positive affect", "no child independent clean up", "v direct concrete inst", "p touching toys for cleanup", "v small mission steps", "no compliance - Passive", "p signal const", "yes compliance", "v positive feedback", "p positive feedback", "v signal const", "v perspective/mirroring", "p mother cleanup", "v concern", "p concern exp", "child positive affect", "v choice", "p gentle touch for clean up", "v rational", "p affection expression", "v motivation arousal", "v unclear",
         "v inadequate perspective/invalidation", "v action oriented feedback", "v affection", "v hostility", "no compliance - Defiance", "p modeling", "v modeling", "p forceful touch for cleanup", "child negative affect", "no compliance - Refusal", "child alert", "no inadequate boundaries setting", "indecisive expectations setting", "legitimazinig expectation violation", "v glorificaion feedback", "v negative cr", "yes child independent clean up", "v threat punishment", "p motivational arrousal", "child tired", "v material reward", "v negative feedback", "unclear compiance"]


def setDfKeysAsBehaviors():
    for key in keysB:
        data[key] = []
    # print(data)
    result = pd.DataFrame(columns=keysB)
    return result
    # df.transpose()
    # print(matrix_input)


def addRowToDfPerFileWithOccurenceNumberPosNeg(filename, dir, turnOperation, *args):
    # print('addRowToDfPerFileWithOccurenceNumber')
    # print('filename = '+filename)
    # print('dir = '+dir)
    args = list(args)
    matrix_input = args[0]

    if filename.endswith(".json"):
        jsonFile = open(dir + '\\' + filename)
        subjectsTurns = json.load(jsonFile)
        subjectsRecord = {}
        subjectName = filename.replace('.json', '')
        subjectsRecord['subjects'] = subjectName
        for turn in subjectsTurns:
            subjectsRecord = turnOperation(
                turn, subjectsRecord, matrix_input)
        result = matrix_input.append(subjectsRecord, ignore_index=True)
        return result
    else:
        return


def countPosNegCodingToTurn(jsonObj, rowObj, matrix_input):
    currBehavior = jsonObj["Code"]
    if not currBehavior in rowObj:
        rowObj[currBehavior] = 0
    rowObj[currBehavior] = rowObj[currBehavior] + 1
    return rowObj


def udateCountsPerBehaviorWithModifiersRow(matrix_input, motherTurnsCount, childTurnsCount, subjectsRow):
    print("udateCountsPerBehaviorWithModifiersRow")
    legend = global_utils.convertLegendCsvToJson()
    # print(keysB)
    # for bKey in keysB:
   # print("len(keysB)="+str(len(keysB)))
    for i in range(len(matrix_input.columns)):
        # for i in range(1):
        currentBehavior = matrix_input.columns[i]
        # print("Checking " + bKey + " i="+str(i) + " motherTurnsCount=" +
        #       str(motherTurnsCount) + " childTurnsCount=" + str(childTurnsCount))
        if (currentBehavior != "subjects"):
            try:
                matrix_input = divideCurrentRowOfSubjects(
                    currentBehavior, legend, matrix_input, motherTurnsCount, childTurnsCount, subjectsRow)
            except Exception as e:
                print(e)
                return
    # print("matrix_input AFTER="+str(matrix_input))
    return matrix_input


def divideCurrentRowOfSubjects(bKey, legend, matrix_input, motherTurnsCount, childTurnsCount, rowNum):
    # only mothers.
    curr = matrix_input.loc[rowNum, bKey]
    if (math.isnan(curr)):
        newCalc = 0
    else:
        newCalc = (matrix_input.loc[rowNum, bKey])/motherTurnsCount
    matrix_input.loc[rowNum, bKey] = newCalc
    return matrix_input


def convertToFrequencyRatioPosNegBehaviours(matrix_input, dir, outputdir):
    print('convertToFrequencyRatioPosNegBehaviours')
    directory = os.fsencode(dir)
    i = 0
    filenames = []
    for file in os.listdir(directory):

        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            subjectCode = filename.replace('.json', '')
            filenames.append(subjectCode)
            print('operating on ' + filename)
            jsonFile = open(dir + filename)
            jsonObjectsArr = json.load(jsonFile)
            mother_dict = [
                x for x in jsonObjectsArr if x['Subject'] == 'mother']
            motherTurnsCount = len(mother_dict)

            child_dict = [x for x in jsonObjectsArr if x['Subject'] == 'child']
            childTurnsCount = len(child_dict)
            # print("matrix_input before loop="+str(matrix_input))
            matrix_input = udateCountsPerBehaviorWithModifiersRow(
                matrix_input, motherTurnsCount, childTurnsCount, i)
            i = i+1

        else:
            continue
    # print('filenames length '+str(len(filenames)))
    # print('matrix_input length '+str(len(matrix_input)))
    # matrix_input['subjects'] = filenames
    # print("matrix_input: ")
    # print(matrix_input)
    matrix_input.to_csv(outputdir +
                        'posNegRatio.csv', index=False)
    print('file posNegRatio.csv was written with calculated matrix')

    return matrix_input


def createFrequencyDfForNegPosCoding(jsonsDir):

    matrix_input = pd.DataFrame(columns=(e.value for e in BehaviorsEmotions))
    matrix_input = global_utils.operateOnJsonFilesForMatrix(addRowToDfPerFileWithOccurenceNumberPosNeg, 'addRowToDfPerFileWithOccurenceNumber',
                                                            jsonsDir, countPosNegCodingToTurn, matrix_input)

    # print("matrix_input: ")
    # print(matrix_input)
    matrix_input.to_csv('behaviorFrequency.csv', index=False)

    return matrix_input


def projectBehaviorFrequencyRatioToTwoDimentions():
    df = pd.read_csv('behaviorsCodesAndFrequencyRatio.csv')
    twoDimDict = {'x': [], 'y': []}
    for index, row in df.iterrows():
        for col in row.keys():
            if (not "Unnamed" in col):
                twoDimDict["x"].append(col)
                twoDimDict["y"].append(row[col])

    twoDimDf = pd.DataFrame(twoDimDict)
    twoDimDf.to_csv("2dimensionsKmeansInput.csv", columns=["x", "y"])


def swapBehaviorAndCodes():
    legendFile = open('legend.json')
    legend = json.load(legendFile)
    legendByBehaviorsName = dict([(value, key)
                                  for key, value in legend["Behavior"].items()])
    print(legendByBehaviorsName)
    return legendByBehaviorsName


# was used for calculating frequency DF
