from utils import convertLegendCsvToJson, loadCsvForSubject, operateOnJsonObjAcrossAllJsonFiles, operateOnJsonFiles, operateOnJsonFilesForMatrix, createCodeRepresenation, get_key
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

    if filename.endswith(".json"):
        jsonFile = open(dir + filename)
        subjectsTurns = json.load(jsonFile)
        subjectsRecord = {}
        subjectName = filename.replace('.json', '')
        subjectsRecord['subjects'] = subjectName
        for turn in subjectsTurns:
            subjectsRecord = jsonObjectOperation(
                turn, subjectsRecord, matrix_input)

        # subjectsRecordSeries = pd.Series(subjectsRecord)
        # pd.concat(
        #     [pd.Series([{'subjects': subjectName}]), subjectsRecordSeries])
        result = matrix_input.append(subjectsRecord, ignore_index=True)
        return result
    else:
        return


def countBehaviorWithModifierToDataRow(jsonObj, rowObj, matrix_input):
    currBehavior = jsonObj["Behavior"]
    if(jsonObj["Modifier_1"] != ""):
        currBehavior = currBehavior+"_" + jsonObj["Modifier_1"]
    if(jsonObj["Modifier_2"] != ""):
        currBehavior = currBehavior+"_" + jsonObj["Modifier_2"]
    if(jsonObj["Modifier_3"] != ""):
        currBehavior = currBehavior+"_" + jsonObj["Modifier_3"]

    if not currBehavior in matrix_input.columns:
        print(currBehavior + ' is not on the matrix')
        newCol = []
        for i in range(len(matrix_input)):
            newCol.append(0)
        matrix_input[currBehavior] = pd.Series(newCol)

    if not currBehavior in rowObj:
        rowObj[currBehavior] = 0
    rowObj[currBehavior] = rowObj[currBehavior] + 1
    return rowObj


def countBehaviorToDataRow(jsonObj, rowObj, matrix_input):
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


def createCorrMatrixPrsnFromDfSpearman(inputFile):
    df = pd.read_csv(inputFile)
    # df = df.astype(int)

    corrMatrix = df.corr(method='spearman')
    print(corrMatrix)
    corrMatrix.to_csv('corrMatrix.csv', index=False)
    sn.heatmap(corrMatrix, annot=True)
    plt.show()
    return df


def createCorrMatrixPrsnFromDfPearson(df, inputFile):
    df = pd.read_csv(inputFile)
    # df = df.astype(int)
    corrMatrix = df.corr(method='pearson')
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
    print('createCoorMatrixWithPvalues')
    # df = df.astype(int)
    pvalues = calculate_pvalues(df)
    pvalues.to_csv('behaviorCountsPvalues.csv', index=False)
    print(pvalues)


def calcKmeans():
    df = pd.read_csv("2dimensionsKmeansInput.csv", usecols=["x", "y"])
    df.plot.scatter(
        x='x', y='y', title="Scatter plot between two variables X and Y")

    plt.show(block=True)
    kmeans = KMeans(n_clusters=7).fit(df)
    centroids = kmeans.cluster_centers_
    print(centroids)

    plt.scatter(df['x'], df['y'], c=kmeans.labels_.astype(
        int), s=50, alpha=0.5)
    plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
    plt.show()


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


def udateCountsPerBehaviorWithModifiersRow(matrix_input, motherTurnsCount, childTurnsCount, rowNum):
    print("udateCountsPerBehaviorWithModifiersRow")
    legend = convertLegendCsvToJson()
    # print(keysB)
    # for bKey in keysB:
   # print("len(keysB)="+str(len(keysB)))
    for i in range(len(matrix_input.columns)):
        # for i in range(1):
        bKey = matrix_input.columns[i]
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
    # print('bKey before is ' + bKey)
    bKeyForFindSubject = bKey.replace('_mother positive tone', '')
    bKeyForFindSubject = bKeyForFindSubject.replace(
        '_mother positive tone_control', '')
    bKeyForFindSubject = bKeyForFindSubject.replace(
        '_mother negative tone_control', '')
    bKeyForFindSubject = bKeyForFindSubject.replace(
        '_mother negative tone', '')
    bKeyForFindSubject = bKeyForFindSubject.replace('_control', '')
    bKeyForFindSubject = bKeyForFindSubject.   replace(
        '_passive non compliance', '')
    bKeyForFindSubject = bKeyForFindSubject.replace(
        '_defiance', '')
    bKeyForFindSubject = bKeyForFindSubject.replace(
        '_refusal', '')

    # print('bKey after is ' + bKeyForFindSubject)
    loc = legend.loc[legend['Behavior'] == bKeyForFindSubject]

    # print("loc[Subject]="+str(loc["Subject"]) +
    #       " " + str(not loc["Subject"].empty))

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


def prepareKmeansInput(df):
    print('prepareKmeansInput')
    dir = 'jsons//'
    directory = os.fsencode(dir)
    i = 0
    for file in os.listdir(directory):
        legendFile = open('legend.json')
        legend = json.load(legendFile)

        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            print('operating on ' + filename)
            jsonFile = open(dir + filename)
            jsonObjectsArr = json.load(jsonFile)
            for jsonObj in jsonObjectsArr:
                behavior = jsonObj.Behavior
                code = get_key(jsonObj, behavior)
                result = df.append(code, ignore_index=True)
        else:
            continue

    print("prepareKmeansInput: ")
    print(df)

    return df


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


def convertToFrequencyRatioWithModifiers(matrix_input):
    print('convertToFrequencyRatio')
    dir = 'jsons//'
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
    matrix_input.to_csv(
        'behaviorWithModifiersFrequencyByTurnRatio.csv', index=False)

    return matrix_input


def convertToFrequencyRatioBySubject(subject):
    print('convertToFrequencyRatio')
    dir = 'jsons//'
    directory = os.fsencode(dir)
    allInteractions = {}
    i = 0
    for file in os.listdir(directory):

        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            print('operating on ' + filename)

            interactionFile = open(dir + filename)
            turnsArray = json.load(interactionFile)
            allSubjectBehaviorsCountPerInteraction = {}
            allInteractions[filename.replace(
                '.json', '')] = allSubjectBehaviorsCountPerInteraction

            subjectTurnsArr = [
                x for x in turnsArray if x['Subject'] == subject]
            subjectTurnsCount = len(subjectTurnsArr)

            for behavior in keysB:
                allSubjectBehaviorsCountPerInteraction[behavior] = 0

            for subjectTurn in subjectTurnsArr:  # count number of behaviors across all turns of this subject
                turnBehavior = subjectTurn['Behavior']
                allSubjectBehaviorsCountPerInteraction[
                    turnBehavior] = allSubjectBehaviorsCountPerInteraction[turnBehavior] + 1

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


def createFrequencyDfWithModifiers():

    matrix_input = pd.DataFrame()
    matrix_input = operateOnJsonFilesForMatrix(addRowToDfPerFileWithOccurenceNumber, 'addRowToDfPerFileWithOccurenceNumber',
                                               "jsons//", countBehaviorWithModifierToDataRow, matrix_input)

    # print("matrix_input: ")
    # print(matrix_input)
    matrix_input.to_csv('behaviorFrequency.csv', index=False)

    return matrix_input


def plotCorrMatrix():
    df = pd.read_csv('corrMatrix.csv')
    newNames = swapBehaviorAndCodes()
    df = df.rename(columns=newNames)
    df.to_csv('behaviorsCodesAndFrequencyRatio.csv')
    print(df)


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


# mat = createFrequencyDf() was used for calculating frequency DF
mat = createFrequencyDfWithModifiers()
print(mat)
print(len(mat))
mat = convertToFrequencyRatioWithModifiers(mat)
# mat = convertToFrequencyRatio(mat) #already written to behaviorFrequencyByTurnRatio.csv
# df = createCorrMatrixPrsnFromDfSpearman('behaviorFrequencyByTurnRatio.csv')
# createCoorMatrixWithPvalues(df)
# calcKmeans(mat)
# projectBehaviorFrequencyRatioToTwoDimentions()
# calcKmeans()
