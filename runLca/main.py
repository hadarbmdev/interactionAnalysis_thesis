from py.runLca.utils import runMplus, analyzeOutput, prepareInputFile, rollBehaviors
import pathlib
import sys
import os
import time


def main():
    error = ""
    iter = 0
    for i in range(3, 6):

        vars_permutations = rollBehaviors(i)

        for vars in vars_permutations:
            iter = iter + 1
            time.sleep(2)
            print(str(iter) + ' :running mplus on vars: '+str(vars))
            try:
                prepareInputFile(vars)
                runMplus()
                analyzeOutput(iter)
                print('done iteration '+str(iter))
            except Exception as e:
                error += ('\n failed vars' + str(vars))
                error += ('\n' + str(e))
                text_file = open("C:\\TEMP\\mplus\\errors.txt", "w")
                n = text_file.write(error)
                text_file.close()


main()
