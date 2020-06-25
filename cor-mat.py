from utils import convertLegendCsvToJson, loadCsvForSubject, operateOnJsonObjAcrossAllJsonFiles, operateOnJsonFiles, operateOnJsonFilesForMatrix
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
    # print('
    #  key ' + key)
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
    corrMatrix = df.corr(method='pearson')
    # print(corrMatrix)
    sn.heatmap(corrMatrix, annot=True)
    plt.show()


def createCorrMatrixPrsnFromDf(df):
    df.to_csv('behaviorCounts.csv', index=False)
    df = df.astype(int)

    corrMatrix = df.corr(method='spearman')
    print(corrMatrix)
    corrMatrix.to_csv('corrMatrix.csv', index=False)
    sn.heatmap(corrMatrix, annot=True)
    plt.show()


def calculate_pvalues(df):
    df = df.dropna()._get_numeric_data()
    dfcols = pd.DataFrame(columns=df.columns)
    pvalues = dfcols.transpose().join(dfcols, how='outer')
    for r in df.columns:
        for c in df.columns:
            pvalues[r][c] = round(spearmanr(df[r], df[c])[1], 4)
    return pvalues


def createCoorMatrixWithPvalues(df):
    df = df.astype(int)
    pvalues = calculate_pvalues(df)
    pvalues.to_csv('behaviorCountsPvalues.csv', index=False)
    print(pvalues)


def calcKmeans(df):
    km = KMeans(n_clusters=7, random_state=0).fit(df)
    print(km)
    y_kmeans = km.predict(df)
    plt.scatter(df[:, 0], df[:, 1], c=y_kmeans, s=50, cmap='viridis')
    centers = km.cluster_centers_
    plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)


def udateCountsPerBehaviorRow(matrix_input, motherTurnsCount, childTurnsCount, rowNum):
    print("udateCountsPerBehaviorRow")
    legend = convertLegendCsvToJson()
    # print(keysB)
    # for bKey in keysB:
   # print("len(keysB)="+str(len(keysB)))
    for i in range(len(keysB)):
        # for i in range(1):
        bKey = keysB[i]
        # print("Checking " + bKey + " i="+str(i) + " motherTurnsCount=" +
        #       str(motherTurnsCount) + " childTurnsCount=" + str(childTurnsCount))

        try:
            matrix_input = divideCurrentRowOfSubjects(
                bKey, legend, matrix_input, motherTurnsCount, childTurnsCount, rowNum)
        except Exception as e:
            print(e)
            return
    # print("matrix_input AFTER="+str(matrix_input))
    return matrix_input


def divideCurrentRowOfSubjects(bKey, legend, matrix_input, motherTurnsCount, childTurnsCount, rowNum):
    # print("matrix_input = "+str(matrix_input))
    loc = legend.loc[legend['Behavior'] == bKey]
    # print("loc[Subject]="+str(loc["Subject"])
    #       + " " + str(not loc["Subject"].empty))
    if (not loc["Subject"].empty):
        if ((loc["Subject"] == "Child").bool()):
            curr = matrix_input.loc[rowNum, bKey]
            newCalc = (matrix_input.loc[rowNum, bKey])/childTurnsCount

            # if ((newCalc != 0) and (newCalc-int(newCalc)) == 0):
            # print("Problems? newCalc="+str(newCalc)+" key=" + str(bKey) + " childTurnsCount="+str(childTurnsCount) +
            #       " matrix_input.loc[rowNum, key])="+str(matrix_input.loc[rowNum, bKey]) + " rowNum = "+str(rowNum))
            matrix_input.loc[rowNum, bKey] = newCalc
        else:
            if ((loc["Subject"] == "Mother").bool()):
                curr = matrix_input.loc[rowNum, bKey]
                newCalc = (matrix_input.loc[rowNum, bKey])/motherTurnsCount

                # if ((newCalc != 0) and (newCalc-int(newCalc)) == 0):
                # print("newCalc="+str(newCalc)+" key=" + str(bKey) + " motherTurnsCount="+str(motherTurnsCount) +
                #       " matrix_input.loc[rowNum, key])="+str(matrix_input.loc[rowNum, bKey]) + " rowNum = "+str(rowNum))
                matrix_input.loc[rowNum, bKey] = newCalc
            else:
                print("Could not find " + loc["Subject"])
    return matrix_input


def convertToFrequencyRatio(matrix_input):
    print('convertToFrequencyRatio')
    dir = 'jsons//'
    directory = os.fsencode(dir)
    i = 0
    for file in os.listdir(directory):

        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            print('operating on ' + filename)
            jsonFile = open(dir + filename)
            jsonObjectsArr = json.load(jsonFile)
            mother_dict = [
                x for x in jsonObjectsArr if x['Subject'] == 'mother']
            motherTurnsCount = len(mother_dict)

            child_dict = [x for x in jsonObjectsArr if x['Subject'] == 'child']
            childTurnsCount = len(child_dict)
            # print("matrix_input before loop="+str(matrix_input))
            matrix_input = udateCountsPerBehaviorRow(
                matrix_input, motherTurnsCount, childTurnsCount, i)
            i = i+1
        else:
            continue

    # print("matrix_input: ")
    # print(matrix_input)
    matrix_input.to_csv('behaviorFrequencyByTurnRatio.csv', index=False)

    return matrix_input


def createFrequencyDf():

    matrix_input = pd.DataFrame(columns=keysB)
    matrix_input = operateOnJsonFilesForMatrix(addRowToDfPerFileWithOccurenceNumber, 'addRowToDfPerFileWithOccurenceNumber',
                                               "jsons//", countBehaviorToDataRow, matrix_input)

    # print("matrix_input: ")
    # print(matrix_input)
    matrix_input.to_csv('behaviorFrequency.csv', index=False)

    return matrix_input


 mat = createFrequencyDf() was used for calculating frequency DF
 mat = convertToFrequencyRatio(mat) #already written to behaviorFrequencyByTurnRatio.csv
print(mat)
# calcKmeans(mat)
