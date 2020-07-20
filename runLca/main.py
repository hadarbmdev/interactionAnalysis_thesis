from py.runLca.utils import runMplus, analyzeOutput, prepareInputFile, rollBehaviors
import pathlib
import sys
import os
import time


def main():
    error = ""
    for i in range(3, 6):
        vars_permutations = rollBehaviors(i)

        for vars in vars_permutations:

            print('running mplus on vars: '+str(vars))
            try:
                prepareInputFile(vars)
                runMplus()
                analyzeOutput()
            except Exception as e:
                error.append('\nfailed vars' + vars)
                error.append('\n' + e)


main()
