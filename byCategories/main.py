from py import global_utils
from py.byCategories.utils import setCodeEntry
from py.byCategories.cor_mat import createFrequencyDf, convertToFrequencyRatio
import pathlib
import sys
import os


def main():

    folderRelativePath = 'py/byCategories/'
    currDir = str(pathlib.Path(
        folderRelativePath+'/jsons/').absolute())

    jsonsPath = global_utils.getDeocdedDir(currDir)

    outputDir = str(pathlib.Path(
        folderRelativePath+'/output/').absolute())

    outputPath = global_utils.getDeocdedDir(outputDir)

    # global_utils.operateOnJsonFiles(
    #     global_utils.replaceComma, 'replaceComma', jsonsPath, '')

    # global_utils.operateOnJsonFiles(setCodeEntry,
    #                                 "setCodeEntry", jsonsPath,  '')
    # global_utils.operateOnJsonFiles(
    #     global_utils.replaceComma, 'replaceComma', jsonsPath, '')

    mat = createFrequencyDf(jsonsPath)
    mat = convertToFrequencyRatio(mat, jsonsPath, outputPath)


main()
