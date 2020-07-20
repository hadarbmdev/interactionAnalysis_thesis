from py.runLca.utils import runMplus, analyzeOutput, prepareInputFile, rollBehaviors
import pathlib
import sys
import os
import time


def main():
    error = ""
    iter = 0
    for i in range(3, 6):

        vars_permutations = rollBehaviors(6)

        for vars in vars_permutations:
            iter = iter + 1
            time.sleep(3)
            print(str(iter) + ' :running mplus on vars: '+str(vars))
            try:
                prepareInputFile(vars)
                runMplus(vars)
                analyzeOutput(iter, len(vars*2))
                print('done iteration '+str(iter))
            except Exception as e:
                text_file = open("C:\\TEMP\\mplus\\errors.txt", "w")
                error = text_file.read()
                n = text_file.write(
                    "failed vars: "+str(vars)+"\n"+error+"\n"+e)
                text_file.close()


main()
