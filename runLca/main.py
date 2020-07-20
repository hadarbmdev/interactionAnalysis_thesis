from py.runLca.utils import runMplus, analyzeOutput, prepareInputFile, rollBehaviors
import pathlib
import sys
import os
import time


def main():
    error = ""
    iter = 0

    file = open("C:\\TEMP\\mplus\\errors.txt", "r+")
    file. truncate(0)
    file. close()

    for i in range(3, 6):

        vars_permutations = rollBehaviors(i)

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
                text_file.write(
                    "failed vars: "+str(vars)+"\n"+"error:"+"\n"+e)
                text_file.close()


main()
