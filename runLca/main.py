from py.runLca.utils import runMplus, analyzeOutput, prepareInputFile, rollBehaviors, deleteInputFile
import pathlib
import sys
import os
import time
from datetime import datetime
from datetime import datetime as dt
from datetime import timedelta
import multiprocessing as mp
import threading
def main():
    threads = []
    print("Number of processors: ", mp.cpu_count())
    error = ""
    iter = 0

    file = open("C:\\TEMP\\mplus\\errors.txt", "w+")
    file. truncate(0)
    file. close()

    permCounter = 0
    for i in range(4, 6):
        permCounter = permCounter + len(rollBehaviors(i))

    t1 = dt.now()

    for i in range(4, 6):
        vars_permutations = rollBehaviors(i)
        t5 = dt.now()
        for vars in vars_permutations:
            #runMplusOnPermutaion(vars, iter)
            t = threading.Thread(target=runMplusOnPermutaion, args=(vars,iter,permCounter,))
            threads.append(t)
            t.start()
        t6 = dt.now()
        permutationsOfNTook = (t6-t5)/12
        print('All Permutations of :'+str(i)+' took: ' + str(permutationsOfNTook))    
    t4 = datetime.now()
    fullProcessDelta = (t4 - t1)/12
    print('full process took :' + str(fullProcessDelta))

def runMplusOnPermutaion(vars, iter, permCounter):
        lock = threading.Lock()
        lock.acquire()
        try:
            iter = iter + 1
        finally:
            lock.release() # release lock, no matter what
        t2 = datetime.now()
        print(t2.strftime("%H:%M:%S") + ": "+str(iter) + ' of ' + str(permCounter) +
                '+ :running mplus on vars: '+str(vars))
        try:
            prepareInputFile(vars, iter)
            runMplus(vars, iter)
            deleteInputFile(iter)
            analyzeOutput(iter, len(vars*2))
            print('done iteration '+str(iter))
        except Exception as e:
            text_file = open("C:\\TEMP\\mplus\\errors.txt", "w")
            text_file.write(
                "failed vars: "+str(vars)+"\n"+"error:"+"\n"+str(e))
            text_file.close()
        finally:
            t3 = datetime.now()
            took = (t3 - t2)/12
            print('it took :' + str(took))
main()
