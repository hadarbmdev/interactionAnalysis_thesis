from utils import loadCsvForSubject, operateOnJsonObjAcrossAllJsonFiles, operateOnJsonFiles, operateOnJsonFilesForMatrix
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

data = {}
#matrix_input = pd.DataFrame(data)

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


def addRowToDfPerFileWithOccurenceNumber(filename, dir, jsonObjectOperation, *args):
    # print('addRowToDfPerFileWithOccurenceNumber')
    # print('filename = '+filename)
    # print('dir = '+dir)
    args = list(args)
    matrix_input = args[0]
    jsonFile = open(dir + filename)
    jsonObjectsArr = json.load(jsonFile)
    rowObj = {}
    for key in keysB:
        rowObj[key] = 0
    for jsonObj in jsonObjectsArr:
        rowObj = jsonObjectOperation(jsonObj, rowObj)

        # currBehavior = jsonObj["Behavior"]
        # if not currBehavior in rowObj:
        #     rowObj[currBehavior] = 0
        # rowObj[currBehavior] = rowObj[currBehavior] + 1
    #dfRow = pd.DataFrame.from_dict(rowObj, orient='index')
    # print('rowObj ')
    # print(rowObj)
    # dfRow.transpose()
   # print('behavior matrix for file ' + filename + str(dfRow))

    # print('args[0] '+str(args[0]))
    # print(dfRow)
    # print('**********')
    result = matrix_input.append(rowObj, ignore_index=True)

    return result


def countBehaviorToDataRow(jsonObj, rowObj):
    currBehavior = jsonObj["Behavior"]
    if not currBehavior in rowObj:
        rowObj[currBehavior] = 0
    rowObj[currBehavior] = rowObj[currBehavior] + 1
    return rowObj


def parseObjToDF(*args):
    args = list(args)
    filename = args[0]
    jsonObj = args[1]
    args = args[2]
    key = jsonObj["Behavior"]
    # print('checking key ' + key)
    if (not key in data):
        data[key] = set()
    data[key].add(filename)


def loadCodesIntoDFAndCsv():

    operateOnJsonObjAcrossAllJsonFiles(
        parseObjToDF, 'parseObjToData', 'jsons//')
    print(data)

    # df = pd.DataFrame(data)
    df = pd.DataFrame.from_dict(data, orient='index')
    # df.transpose()
    print(df)
    df.to_csv('input_4_correlation_matrix.csv')

# loadCodesIntoDFAndCsv()


def loadMatrixCorrInputFromCsv():
    df = pd.read_csv('input_4_correlation_matrix_transposed.csv')
    # print(df)
    corrMatrix = df.corr(method='spearman')
    # print(corrMatrix)
    sn.heatmap(corrMatrix, annot=True)
    plt.show()


def createCorrMatrixPrsnFromDf(df):
    df = df.astype(int)

    corrMatrix = df.corr(method='spearman')
    print(corrMatrix)
    sn.heatmap(corrMatrix, annot=True)
    plt.show()


def createFrequencyDf():

    matrix_input = pd.DataFrame(columns=keysB)
    matrix_input = operateOnJsonFilesForMatrix(addRowToDfPerFileWithOccurenceNumber, 'addRowToDfPerFileWithOccurenceNumber',
                                               "jsons//", countBehaviorToDataRow, matrix_input)

    #print("matrix_input: ")
    # print(matrix_input)
    return matrix_input


mat = createFrequencyDf()
createCorrMatrixPrsnFromDf(mat)
