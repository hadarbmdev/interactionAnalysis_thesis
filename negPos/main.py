from py import global_utils
from py.negPos.utils import setBehaviorAndEmotionEntry, setBehaviorAndEmotionEntryForObj, divideCurrentRowOfSubjects
import pathlib
import sys
import os


def main():
    folderRelativePath = 'py/negPos/'
    jsonsDir = str(pathlib.Path(
        folderRelativePath+'/jsons/').absolute())

    jsonsPath = global_utils.getDeocdedDir(jsonsDir)

    outputDir = str(pathlib.Path(
        folderRelativePath+'/output/').absolute())

    outputPath = global_utils.getDeocdedDir(outputDir)

    global_utils.operateOnJsonFiles(
        global_utils.replaceComma, 'replaceComma', jsonsPath, '')
    global_utils.operateOnJsonFiles(setBehaviorAndEmotionEntry,
                                    "setCodeEntry", jsonsPath, setBehaviorAndEmotionEntryForObj)
    global_utils.operateOnJsonFiles(
        global_utils.replaceComma, 'replaceComma', jsonsPath, '')

    mat = global_utils.createFrequencyDf(jsonsDir)
    print(mat)
    print(len(mat))
    mat = global_utils.convertToFrequencyRatio(
        mat, jsonsPath, outputPath, 'negPosFrequency.csv', divideCurrentRowOfSubjects)


main()
