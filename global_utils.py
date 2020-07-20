import sys
import enum
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import json
from operator import itemgetter
import os
import fileinput
import pathlib


def getLegend():
    folderRelativePath = 'py/'
    legendFile = str(pathlib.Path(
        folderRelativePath+'/legend.json').absolute())
    legendFile = open(legendFile)
    legend = json.load(legendFile)
    return legend


def convertLegendCsvToJson():
    filename = 'Legend.csv'

    try:
        result = pd.read_csv(filename)
        result.to_json('legend.json')
        return result
    except Exception as e:
        print("Oops! could not read file " +
              filename, e.__class__, "occurred.")
        print("Next entry.")
        print()
        return None

    return


def drawChartMotherAndChild(dfMother, dfChild, pos, title):
    # dfMother['Code'] = pd.to_numeric(dfMother['Code'], errors='coerce')
    # dfChild['Code'] = pd.to_numeric(dfChild['Code'], errors='coerce')
    dfMother.sort_values(by='start date')
    dfChild.sort_values(by='start date')

    pos.plot('start date', 'Code', data=dfMother, marker='o', markerfacecolor='blue',
             markersize=5, color='skyblue', linewidth=1)
    pos.plot('start date', 'Code', data=dfChild, marker='o', markerfacecolor='red',
             markersize=5, color='red', linewidth=1)

    pos.suptitle = str(title)
# s = pd.Series(dfMother['start date'], dfChild['start date'])
# s.unique()
# pos.plot(s, dfMother['Code'], marker='o',
#          linestyle='--', color='r', label='Square')
# pos.xlabel('time')
# pos.ylabel('code')
# pos.xticks(s, dfMother['Code'])
# pos.title(title)
# pos.legend()


def swapBehaviorAndCodes():
    legendFile = open('legend.json')
    legend = json.load(legendFile)
    legendByBehaviorsName = dict([(value, key)
                                  for key, value in legend["Behavior"].items()])
    # print(legendByBehaviorsName)
    return legendByBehaviorsName


def dateparser(x): return datetime.strptime(x, '%H:%M:%S')


def loadCsvForSubject(prefix, participantsCode, subject, dateColName, filePath):
    filename = filePath + prefix+participantsCode+subject+'.csv'

    try:
        result = pd.read_csv(filename, parse_dates=[
                             dateColName], date_parser=dateparser)
        return result
    except Exception as e:
        print("Oops! could not read file " +
              filename, e.__class__, "occurred.")
        print("Next entry.")
        print()
        return None


def loadJsonForSubject(prefix, participantsCode, subject, dateColName, filePath):
    filename = filePath + prefix+participantsCode+subject+'.json'

    try:
        jsonFile = open(filename)
        obj = json.load(jsonFile)
        result = pd.DataFrame(obj)
        print(subject + " " + participantsCode)
        print(result)
        return result
    except Exception as e:
        print("Oops! could not read file " +
              filename, e.__class__, "occurred.")
        print("Next entry.")
        print()
        return None


def prepareCsvForSubject(srcFile, targetJsonPath):
    targetPath = 'output\\'
    motherObj = {
        "start date": [],
        "Code": []
    }
    childObj = {
        "start date": [],
        "Code": []
    }

    filename = os.fsdecode(srcFile)
    start = filename.index('_')+1
    end = filename.index('.')
    subjectCode = filename[start:end]
    print('subjectCode = ' + subjectCode)
    if filename.endswith(".json"):
        print('preparing csv from ' + targetJsonPath + filename)
        jsonFile = open(targetJsonPath + filename, 'r')
        allJsonObjs = json.load(jsonFile)
        newArr = []
        timeStampInt = 1
        for jsonObj in allJsonObjs:
            if (jsonObj["Subject"] == "mother"):
                timeStampInt = timeStampInt+1
                motherObj["start date"].append(jsonObj["Time_Relative_hms"])
                # motherObj["start date"].append(timeStampInt)
                motherObj["Code"].append(jsonObj["Code"])

            if (jsonObj["Subject"] == "child"):

                childObj["start date"].append(jsonObj["Time_Relative_hms"])
                # childObj["start date"].append(j)
                childObj["Code"].append(jsonObj["Code"])

        jsonFileMother = open(targetPath + 'liya' +
                              subjectCode + 'mother.json', 'w')
        jsonFileChild = open(targetPath + 'liya' +
                             subjectCode + 'child.json', 'w')
        # print('dumping ' + str(allJsonObjs))
        jsonFileMother.write(str(motherObj))
        jsonFileChild.write(str(childObj))


def getParticipantsCode(*args):
    codes = []

    def getSubjectCodeFromFileName(sFile, output, *args):
        filename = os.fsdecode(sFile)
        print(filename)
        return codes.append(
            filename[filename.index('_')+1:filename.index('.')])
    operateOnJsonFiles(getSubjectCodeFromFileName,
                       "getSubjectCodeFromFileName", "jsons//", *args)
    # print(codes)
    return codes


def getKeyForValue(json, lookupValue):
    for key in json.keys():
        if json[key] == lookupValue:
            # print('found key ' + key + ' for lookupValue: "' + lookupValue + '"')
            return key
    return "-1"


def setCodeEntry(jFile, srcPath):
    filename = os.fsdecode(jFile)

    jsonFile = open(targetJsonPath + filename, 'r')
    jsonObjectsArr = json.load(jsonFile)
    for jsonObj in jsonObjectsArr:
        jsonObj = setCodeEntryForObj(jsonObj)
    strArr = str(jsonObjectsArr)
    strArr = strArr.replace("'", '"')
    jsonFile = open(srcPath + filename, 'w')
    jsonFile.write(str(jsonObjectsArr))


def get_key(my_dict, val):
    for key, value in my_dict.items():
        if val == value:
            return key

    return "key doesn't exist"


def setCodeEntryForObj(jsonObj):
    legendFile = open('legend.json')
    legend = json.load(legendFile)

    legendColumnX = "Behavior"
    lookupValue = jsonObj[legendColumnX]
    legendSubTableX = legend[legendColumnX]
    xKey = getKeyForValue(legendSubTableX, lookupValue)
    if (xKey != "-1"):
        legendColumnY = "Group Code"
        # print('looking up in table "' + str(legendColumnY) +'" at key ' + str(xKey))

        legendSubTableY = legend[legendColumnY]
        targetValueY = legendSubTableY[xKey]
        # print('... found: ' + str(targetValueY))

        if (not "Code" in jsonObj):
            jsonObj["Code"] = -1
        jsonObj["Code"] = targetValueY
    else:
        print('did not find key for lookupValue: "' +
              (lookupValue) + '" on column ' + legendColumnX)

    return jsonObj


def createCodeRepresenation():
    legendFile = open('legend.json')
    legend = json.load(legendFile)

    legendColumnX = "Behavior"
    jsonObj = {}
    for item in legend:
        behavior = legend["Behavior"]
        print("behavior="+str(behavior))
        code = legend["Code"]
        if not jsonObj[behavior]:
            jsonObj[behavior] = ""
        jsonObj[behavior] = code

    print("behavior codes: "+str(jsonObj))
    return jsonObj


def getDeocdedDir(dir):
    decodedPath = dir.encode(sys.getfilesystemencoding()).decode(
        sys.getfilesystemencoding()) + '/'
    return decodedPath


def replaceComma(jsonFile, targetJsonPath, *args):
    filename = os.fsdecode(jsonFile)
    with fileinput.FileInput(targetJsonPath + filename, inplace=True, backup=None) as file:
        for line in file:
            print(line.replace("'", '"'), end='')


def operateOnJsonFile(filename, dir, jsonObjectOperation, *args):
    print('operateOnJsonFile')
    print('filename = '+filename)
    jsonFile = open(dir + filename)
    jsonObjectsArr = json.load(jsonFile)
    for jsonObj in jsonObjectsArr:
        jsonObj = jsonObjectOperation(filename, jsonObj, *args)
    return


def operateOnJsonFiles(fileOperation, operationName, dir, jsonObjectOperation, *args):
    print('operateOnJsonFiles')
    directory = os.fsencode(dir)
    data = {}
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            print('operating '+operationName + ' on ' + filename)
            # operation(file, dir, operationParams)
            fileOperation(filename, dir, jsonObjectOperation, *args)

        else:
            continue
    print('done '+operationName+'()')


def operateOnJsonFilesForMatrix(fileOperation, operationName, dir, jsonObjectOperation, *args):
    print('operateOnJsonFilesForMatrix')
    directory = os.fsencode(dir)
    data = {}
    args = list(args)
    matrix_input = args[0]

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            print('operating '+operationName + ' on ' + filename)
            # operation(file, dir, operationParams)
            result = fileOperation(
                filename, dir, jsonObjectOperation, *args)
            matrix_input = matrix_input.append(result, ignore_index=True)

        else:
            continue
    print('done '+operationName+'()')
    return matrix_input


def operateOnJsonObjAcrossAllJsonFiles(jsonObjectOperation, operationName, dir, *args):
    operateOnJsonFiles(operateOnJsonFile, operationName,
                       dir, jsonObjectOperation, *args)
