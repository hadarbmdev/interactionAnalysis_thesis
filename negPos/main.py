from py import global_utils
from py.negPos.utils import setBehaviorAndEmotionEntry
from py.negPos.cor_mat import createFrequencyDfForNegPosCoding, convertToFrequencyRatioPosNegBehaviours
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

    # global_utils.operateOnJsonFiles(
    #     global_utils.replaceComma, 'replaceComma', jsonsPath, '')
    # global_utils.operateOnJsonFiles(setBehaviorAndEmotionEntry,
    #                                 "setBehaviorAndEmotionEntry", jsonsPath,  '')
    # global_utils.operateOnJsonFiles(
    #     global_utils.replaceComma, 'replaceComma', jsonsPath, '')

    mat = createFrequencyDfForNegPosCoding(jsonsDir)
    print(mat)
    print(len(mat))
    mat = convertToFrequencyRatioPosNegBehaviours(mat, jsonsPath, outputPath)


main()
