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
targetJsonPath = 'jsons/'


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


def drawPlotForMotherAndChild(participantsCode, filePath, col):
    strCode = str(participantsCode)

    if (len(participantsCode) < 3):
        strCode = "0"+strCode
    # print('loading data for participatns ' + participantsCode)
    dfMother = loadJsonForSubject(
        'liya', strCode, 'mother', 'start date', filePath)
    dfChild = loadJsonForSubject(
        'liya', strCode, 'child', 'start date', filePath)

    if ((dfMother is not None) and (dfChild is not None)):
        drawChartMotherAndChild(dfMother, dfChild, col, participantsCode)


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


def drawSubPlotForMotherAndChild(filePath, codes, limit):
    subPlotsNum = min(len(codes), limit)
    print('subPlotsNum = ' + str(subPlotsNum))
    modulo = 1

    for j in range(2, 10):
        if (subPlotsNum % j == 0):
            modulo = j
            break
        #print("modulo is: "+str(modulo))

    print("subPlotsNum/modulo = " + str(subPlotsNum/modulo))
    fig, ax = plt.subplots(nrows=round(subPlotsNum/modulo),
                           ncols=round(subPlotsNum/modulo), figsize=(8, 6))
    i = 1
    for row in ax:
        for col in row:
            if (i > subPlotsNum):
                break
            print(i)
            drawPlotForMotherAndChild(str(codes[i]), filePath, col)
            i = i + 1
    plt.gcf().autofmt_xdate()
    plt.show()


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


def setBehaviorAndEmotionEntry(jFile, srcPath, *args):
    filename = os.fsdecode(jFile)

    jsonFile = open(targetJsonPath + filename, 'r')
    currentInteraction = json.load(jsonFile)
    result = []
    for interactionTurn in currentInteraction:
        interactionTurn = setBehaviorAndEmotionEntryForObj(interactionTurn)
    strArr = str(currentInteraction)
    strArr = strArr.replace("'", '"')
    jsonFile = open(srcPath + filename, 'w')
    jsonFile.write(str(currentInteraction))


def setBehaviorAndEmotionEntryForObj(interactionTurn):
    legendFile = open('legend.json')
    legend = json.load(legendFile)

    legendColumnX = "Behavior"
    lookupValue = interactionTurn[legendColumnX]
    legendSubTableX = legend[legendColumnX]
    # lookup for the key of the selected behavior, in the legent
    xKey = getKeyForValue(legendSubTableX, lookupValue)
    if (xKey != "-1"):
        legendColumnY = "Group Code"
        # print('looking up in table "' + str(legendColumnY) +'" at key ' + str(xKey))

        legendSubTableY = legend[legendColumnY]
        # this is the group of the behavior
        targetValueY = legendSubTableY[xKey]
        behaviorCategory = targetValueY
        # print('... found: ' + str(targetValueY))

        if (not "Code" in interactionTurn):
            interactionTurn["Code"] = -1
        interactionTurn["Code"] = getBehaviorEmotionCodingFromBehaviorCategoryAndModifiers(
            behaviorCategory, interactionTurn['Modifier_1'], interactionTurn['Modifier_2'], interactionTurn['Modifier_3']).value
    else:
        print('did not find key for lookupValue: "' +
              (lookupValue) + '" on column ' + legendColumnX)

    return interactionTurn


# creating enumerations using class


class BehaviorsEmotions(enum.Enum):
    posBposT = 1
    posBnegT = 2
    negBposT = 3
    negBnegT = 4
    posBunknown = 5
    negBunknown = 6


def getBehaviorEmotionCodingFromBehaviorCategoryAndModifiers(behaviorCategory, mod1, mod2, mod3):
    if ((behaviorCategory == "Control") or (behaviorCategory == "Inadequate boundaries setting") or (behaviorCategory == "Hostility") or isControlBehavior(mod1, mod2, mod3)):
        # it will be negativeB. now check the tone
        if(isPostivieTone(mod1, mod2, mod3)):
            return BehaviorsEmotions.negBposT
        if(isNegativeTone(mod1, mod2, mod3)):
            return BehaviorsEmotions.negBnegT
        else:
            return BehaviorsEmotions.negBunknown
    else:  # positibe bahavior. Check for tone
        if(isPostivieTone(mod1, mod2, mod3)):
            return BehaviorsEmotions.posBposT
        if(isNegativeTone(mod1, mod2, mod3)):
            return BehaviorsEmotions.posBnegT
        else:
            return BehaviorsEmotions.posBunknown


def isPostivieTone(mod1, mod2, mod3):
    if ((mod1 == "mother positive tone") or (mod2 == "mother positive tone") or ((mod3 == "mother positive tone"))):
        return True
    else:
        return False


def isControlBehavior(mod1, mod2, mod3):
    return ((mod1 == "control") or (mod2 == "control") or ((mod3 == "control")))


def isNegativeTone(mod1, mod2, mod3):
    if ((mod1 == "mother negative tone") or (mod2 == "mother negative tone") or ((mod3 == "mother negative tone"))):
        return True
    else:
        return False


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
