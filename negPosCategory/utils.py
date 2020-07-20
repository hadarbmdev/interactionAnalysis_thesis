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
from py import global_utils
import math


class BehaviorsEmotions(enum.Enum):
    posBposT = 1
    posBnegT = 2
    negBposT = 3
    negBnegT = 4
    posBunknown = 5
    negBunknown = 6


def divideCurrentRowOfSubjects(bKey, legend, matrix_input, motherTurnsCount, childTurnsCount, rowNum):
    # only mothers.
    curr = matrix_input.loc[rowNum, bKey]
    if (math.isnan(curr)):
        newCalc = 0
    else:
        newCalc = (matrix_input.loc[rowNum, bKey])/motherTurnsCount
    matrix_input.loc[rowNum, bKey] = newCalc
    return matrix_input


def setBehaviorCategoryAndEmotionEntry(jFile, srcPath, *args):

    directory = global_utils.getDeocdedDir(srcPath)
    filename = os.fsdecode(jFile)

    jsonFile = open(directory + filename, 'r')
    currentInteraction = json.load(jsonFile)
    result = []
    args = list(args)
    turnOperation = args[0]

    for interactionTurn in currentInteraction:
        interactionTurn = turnOperation(
            interactionTurn)
    strArr = str(currentInteraction)
    strArr = strArr.replace("'", '"')
    jsonFile = open(srcPath + filename, 'w')
    jsonFile.write(str(currentInteraction))


def setBehaviorCategoryAndEmotionEntryForObj(interactionTurn):
    legend = global_utils.getLegend()

    legendColumnX = "Behavior"
    lookupValue = interactionTurn[legendColumnX]
    legendSubTableX = legend[legendColumnX]
    # lookup for the key of the selected behavior, in the legent
    xKey = global_utils.getKeyForValue(legendSubTableX, lookupValue)
    if (xKey != "-1"):
        legendColumnY = "Behavior Group"
        # print('looking up in table "' + str(legendColumnY) +'" at key ' + str(xKey))

        legendSubTableY = legend[legendColumnY]
        # this is the group of the behavior
        targetValueY = legendSubTableY[xKey]
        behaviorCategory = targetValueY

        # print('... found: ' + str(targetValueY))

        if (not "Code" in interactionTurn):
            interactionTurn["Code"] = ""
        interactionTurn["Code"] = getBehaviorEmotionCodingFromBehaviorCategoryAndModifiers(
            behaviorCategory, interactionTurn['Modifier_1'], interactionTurn['Modifier_2'], interactionTurn['Modifier_3'])
    else:
        print('did not find key for lookupValue: "' +
              (lookupValue) + '" on column ' + legendColumnX)

    return interactionTurn


def getBehaviorEmotionCodingFromBehaviorCategoryAndModifiers(behaviorCategory, mod1, mod2, mod3):
    categoryName = behaviorCategory
    if(isControlBehavior(mod1, mod2, mod3)):
        return categoryName+"_"+"NEG"

    if(isNegativeTone(mod1, mod2, mod3)):
        return categoryName+"_"+"NEG"

    if(isPostivieTone(mod1, mod2, mod3)):
        return categoryName+"_"+"POS"

    else:
        return categoryName+"_"+"UNKNOWN"


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
