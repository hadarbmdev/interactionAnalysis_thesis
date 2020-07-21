from py.runLca.utils import runMplus, analyzeOutput, prepareInputFile, rollBehaviors
import pathlib
import sys
import os
import time
from datetime import datetime
from datetime import datetime as dt
from datetime import timedelta


def main():
    error = ""
    iter = 0

    file = open("C:\\TEMP\\mplus\\errors.txt", "r+")
    file. truncate(0)
    file. close()

    permCounter = 0
    for i in range(3, 6):
        permCounter = permCounter + len(rollBehaviors(i))

    t1 = dt.now()

    for i in range(3, 6):

        vars_permutations = rollBehaviors(i)

        for vars in vars_permutations:
            iter = iter + 1
            time.sleep(3)
            t3 = datetime.now()
            print(t3.strftime("%H:%M:%S") + ": "+str(iter) + ' of ' + str(permCounter) +
                  '+ :running mplus on vars: '+str(vars))
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
            finally:
                t2 = datetime.now()
                took = (t2 - t1)/12
                print('it took :' + str(took.seconds))


main()
