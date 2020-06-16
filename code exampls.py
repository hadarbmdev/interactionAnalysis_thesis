import csv
import json
from operator import itemgetter
import os
import pandas as pd
import fileinput
targetJsonPath = 'jsons/'


def splitToJsonSubject():
    targetJsonPath = 'objectPerSubjectsCode.json'
    sourceJsonPath = 'liya.json'
    data = {}
    fieldnames = ('Date_Time_Absolute_dmy_hmsf', 'Date_dmy', 'Time_Absolute_hms', 'Time_Absolute_f', 'Time_Relative_hmsf', 'Time_Relative_hms', 'Time_Relative_f',
                  'Time_Relative_sf', 'Duration_sf', 'Observation', 'Event_Log', 'Subject', 'Behavior', 'Modifier_1', 'Modifier_2', 'Modifier_3', 'Event_Type')
    targetJson = open(targetJsonPath, 'w')
    pluck = lambda dict, *args: (dict[arg] for arg in args)

    with open(sourceJsonPath) as jsonFile:
        for row in jsonFile:
            obj = json.loads(row)
            Observation = obj['Observation']
            names = ('Time_Relative_hms', 'Duration_sf', 'Subject', 'Behavior',
                     'Modifier_1', 'Modifier_2', 'Modifier_3', 'Event_Type')

            newObj = {key: value for key, value in obj.items()
                      if key in names}

            print('Observation='+(Observation))
            if (not Observation in data):
                data[Observation] = []
            data[Observation].append(newObj)

    json.dump(data, targetJson)


def jsonFilePerSubjectCode():
    targetJsonPath = 'jsons/subjects_'
    sourceJsonPath = 'objectPerSubjectsCode.json'

    jsonFile = open(sourceJsonPath)
    obj = json.load(jsonFile)
    for key in obj.keys():
        print(key)
        targetJson = open(targetJsonPath+key[0:3]+".json", 'w')
        json.dump(obj[key], targetJson)

    print('done')


def extractTimeAndCodePerMotherAndChile():

    directory = os.fsencode('jsons/')
    data = {}
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            jsonFile = open(filename)
            obj = json.load(jsonFile)
            names = ('Time_Relative_hms', 'Code')
            newObj = {key: value for key, value in obj.items()
                      if key in names}
            Subject = obj['Subject']

            if (not Subject in data):
                data[Subject] = []
            data[Subject].append(newObj)
            continue
        else:
            continue
    print('done')


def getKeyForValue(json, lookupValue):
    for key in json.keys():
        if json[key] == lookupValue:
            print('found key ' + key + ' for lookupValue: "' + lookupValue + '"')
            return key
    return "-1"


def workOnEntry(jFile, operation):
    filename = os.fsdecode(jFile)

    jsonFile = open(targetJsonPath + filename, 'r')
    jsonObjectsArr = json.load(jsonFile)
    for jsonObj in jsonObjectsArr:
        jsonObj = operation(jsonObj)
    strArr = str(jsonObjectsArr)
    strArr = strArr.replace("'", '"')
    jsonFile = open(targetJsonPath + filename, 'w')
    jsonFile.write(str(jsonObjectsArr))


def setBehaviorComplianceEntry(jFile):
    filename = os.fsdecode(jFile)

    jsonFile = open(targetJsonPath + filename, 'r')
    jsonObjectsArr = json.load(jsonFile)
    for jsonObj in jsonObjectsArr:
        jsonObj = setBehaviorComplianceEntryForObj(jsonObj)
    strArr = str(jsonObjectsArr)
    strArr = strArr.replace("'", '"')
    jsonFile = open(targetJsonPath + filename, 'w')
    jsonFile.write(str(jsonObjectsArr))


def setBehaviorComplianceEntryForObj(jsonObj):
    if (jsonObj["Behavior"] == "no compliance"):
        if ((jsonObj["Modifier_3"] == "passive non compliance") or (jsonObj["Modifier_2"] == "passive non compliance") or (jsonObj["Modifier_1"] == "passive non compliance")):
            jsonObj["Behavior"] = "no compliance - Passive"
        else:
            if ((jsonObj["Modifier_3"] == "defiance") or (jsonObj["Modifier_2"] == "defiance") or (jsonObj["Modifier_1"] == "defiance")):
                jsonObj["Behavior"] = "no compliance - Defiance"
            else:
                if ((jsonObj["Modifier_3"] == "refusal") or (jsonObj["Modifier_2"] == "refusal") or (jsonObj["Modifier_1"] == "refusal")):
                    jsonObj["Behavior"] = "no compliance - Refusal"
    return jsonObj


def setCodeEntry(jFile):
    filename = os.fsdecode(jFile)

    jsonFile = open(targetJsonPath + filename, 'r')
    jsonObjectsArr = json.load(jsonFile)
    for jsonObj in jsonObjectsArr:
        jsonObj = setCodeEntryForObj(jsonObj)
    strArr = str(jsonObjectsArr)
    strArr = strArr.replace("'", '"')
    jsonFile = open(targetJsonPath + filename, 'w')
    jsonFile.write(str(jsonObjectsArr))


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


def filterEntries(jsonFile):
    filename = os.fsdecode(jsonFile)
    if filename.endswith(".json"):
        print('operating on ' + targetJsonPath + filename)
        jsonFile = open(targetJsonPath + filename, 'r')
        allJsonObjs = json.load(jsonFile)
        newArr = []
        for jsonObj in allJsonObjs:
            if (not filterSingleObjEntries(jsonObj)):
                newArr.append(jsonObj)
        jsonFile = open(targetJsonPath + filename, 'w')
        # print('dumping ' + str(allJsonObjs))
        jsonFile.write(str(newArr))


def replaceComma(jsonFile):
    filename = os.fsdecode(jsonFile)
    with fileinput.FileInput(targetJsonPath + filename, inplace=True, backup=None) as file:
        for line in file:
            print(line.replace("'", '"'), end='')


def filterSingleObjEntries(jsonObj):
    unusedFileds = [
        "yes experimenter",
        "no experimenter",
        "no p affection expression",
        "no p aut sup",
        "no p concern exp",
        "no p const",
        "no p hostility",
        "no p positive feedback",
        "no physical control",
        "no v affection",
        "no v aut sup",
        "no v concern",
        "no v const",
        "no v control",
        "no v feedback",
        "no v hostility",
        "no verbal unclear"
    ]
    for field in unusedFileds:
        if (jsonObj["Behavior"] == field) or (jsonObj["Behavior"] == ""):
            return True
    return False


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


def filterByObserver(observerName):
    targetJsonPath = 'target.json'
    jsonFilePath = 'data.json'
    data = {}
    fieldnames = ('Date_Time_Absolute_dmy_hmsf', 'Date_dmy', 'Time_Absolute_hms', 'Time_Absolute_f', 'Time_Relative_hmsf', 'Time_Relative_hms', 'Time_Relative_f',
                  'Time_Relative_sf', 'Duration_sf', 'Observation', 'Event_Log', 'Subject', 'Behavior', 'Modifier_1', 'Modifier_2', 'Modifier_3', 'Event_Type')
    targetJson = open(targetJsonPath, 'w')
    with open(jsonFilePath) as jsonFile:
        for row in jsonFile:
            obj = json.loads(row)
            Observation = (obj['Observation'])
            if (observerName in Observation):
                json.dump(row, targetJson)
                targetJson.write('\n')


def operateOnJsonFiles(operation, operationName):
    directory = os.fsencode('jsons/')
    data = {}
    targetJsonPath = 'jsons/'
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            print('operating '+operationName + ' on ' + filename)
            operation(file)
        else:
            continue
    print('done '+operationName+'()')


operateOnJsonFiles(filterEntries, "filterEntries")
operateOnJsonFiles(replaceComma, "replaceComma")
