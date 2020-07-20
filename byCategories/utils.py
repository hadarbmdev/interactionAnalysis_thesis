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
import os
import fileinput
from py import global_utils


def setCodeEntry(jFile, srcPath, *args):

    directory = global_utils.getDeocdedDir(srcPath)
    filename = os.fsdecode(jFile)

    jsonFile = open(directory + filename, 'r')
    jsonObjectsArr = json.load(jsonFile)
    for jsonObj in jsonObjectsArr:
        jsonObj = setCodeEntryForObj(jsonObj)
    strArr = str(jsonObjectsArr)
    strArr = strArr.replace("'", '"')
    jsonFile = open(srcPath + filename, 'w')
    jsonFile.write(str(jsonObjectsArr))


def setCodeEntryForObj(jsonObj):
    legend = global_utils.getLegend()

    legendColumnX = "Behavior"
    lookupValue = jsonObj[legendColumnX]
    legendSubTableX = legend[legendColumnX]
    xKey = global_utils.getKeyForValue(legendSubTableX, lookupValue)
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
