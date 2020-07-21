from py.runLca.utils import runMplus, analyzeOutput, prepareInputFile, rollBehaviors, deleteInputAndOutpusFiles
import pathlib
import sys
import os
import time
from datetime import datetime
from datetime import datetime as dt
from datetime import timedelta
import multiprocessing as mp
from multiprocessing import Process, freeze_support
import threading
import logging
class Counter(object):
    def __init__(self, start=0):
        self.lock = threading.Lock()
        self.value = start
    def increment(self):
        logging.debug('Waiting for lock')
        self.lock.acquire()
        try:
            logging.debug('Acquired lock')
            self.value = self.value + 1
        finally:
            self.lock.release()

def main():
    if __name__ == '__main__':
        # freeze_support()
        counter = Counter()
        threads = []
        maximumNumberOfThreads = 2
        print("Number of processors: ", mp.cpu_count())
        error = ""
        

        file = open("C:\\TEMP\\mplus\\errors.txt", "w+")
        file. truncate(0)
        file. close()
        
        
        threadLimiter = threading.BoundedSemaphore(maximumNumberOfThreads)
        permCounter = 0
        for i in range(3, 6):
            permCounter = permCounter + len(rollBehaviors(i))

        t1 = dt.now()

        for i in range(43 6):
            vars_permutations = rollBehaviors(i)
            t5 = dt.now()
            for vars in vars_permutations:
                #runMplusOnPermutaion(vars, iter)
                threadLimiter.acquire()
                try:
                    t = threading.Thread(target=runMplusOnPermutaion, args=(vars,counter,permCounter,))
                    threads.append(t)
                    t.start()
                finally:
                    threadLimiter.release()
            logging.debug('Waiting for worker threads')
            main_thread = threading.currentThread()
            for t in threading.enumerate():
                if t is not main_thread:
                    t.join()
            logging.debug('Counter: %d', counter.value)
            t6 = dt.now()
            permutationsOfNTook = (t6-t5)/12
            print('All Permutations of :'+str(i)+' took: ' + str(permutationsOfNTook))    
        t4 = datetime.now()
        fullProcessDelta = (t4 - t1)/12
        print('full process took :' + str(fullProcessDelta))

def runMplusOnPermutaion(vars, c, permCounter):
        lock = threading.Lock()
        c.increment()
        print('THIS THREAD IS WORKING ON COUNTER '+str(c.value))
        t2 = datetime.now()
        print(t2.strftime("%H:%M:%S") + ": "+str(c.value) + ' of ' + str(permCounter) +
                '+ :running mplus on vars: '+str(vars))
        try:
            prepareInputFile(vars, c.value)
            runMplus(vars, c.value)
            analyzeOutput(c.value, len(vars*2))
            deleteInputAndOutpusFiles(c.value)
            print('done iteration '+str(c.value))
            return
        except Exception as e:
            lock.acquire()
            try:
                text_file = open("C:\\TEMP\\mplus\\errors.txt", "w")
                text_file.write(
                    "failed vars: "+str(vars)+"\n"+"error:"+"\n"+str(e))
                text_file.close()
            finally:
                lock.release() # release lock, no matter what
            
        finally:
            t3 = datetime.now()
            took = (t3 - t2)/12
            print('it took :' + str(took))
 
 
# pool = mp.Pool(mp.cpu_count())
# if __name__ == "__main__":
#     freeze_support()
#     pool.apply(main, args=())
# pool.close()   
main()
