from subprocess import Popen, PIPE, call, check_call
import os
import math
import shutil
import itertools
import threading
import csv

behaviors = ["vdirePT", "p_touchi", "vsmalpt", "p_signal", "vpsfdpt", "p_positi", "vsglpt", "vperspt", "vcncrpt", "p_concer", "v_choice", "p_gentle", "v_ration", "p_affect", "v_motiva", "pgenC", "v_inadeq",
             "v_action", "vafectpt", "vhostlpt", "p_modeli", "vmdlpt", "vdirptc", "csmlntc", "psgnC", "v_modeli", "vdirNTC", "vsmNTC", "p_forcef", "indecisi", "legitima", "v_glorif", "vngcrpt", "vsgnptc", "childInd", "p_motiva"]
behaviors_extended = ["v direct concrete inst_mother positive tone", "p touching toys for cleanup", "v small mission steps_mother positive tone", "p signal const", "v positive feedback_mother positive tone", "p positive feedback", "v signal const_mother positive tone", "v perspective/mirroring_mother positive tone", "v concern_mother positive tone", "p concern exp", "v choice_mother positive tone", "p gentle touch for clean up", "v rational_mother positive tone", "p affection expression", "v motivation arousal_mother positive tone", "p gentle touch for clean up_control", "v inadequate perspective/invalidation_mother positive tone", "v action oriented feedback_mother positive tone", "v affection_mother positive tone",
                      "v hostility_mother positive tone", "p modeling", "v modeling_mother positive tone", "v direct concrete inst_mother positive tone_control", "v small mission steps_mother negative tone_control", "p signal const_control", "v modeling_mother negative tone", "v direct concrete inst_mother negative tone_control", "v small mission steps_mother positive tone_control", "p forceful touch for cleanup", "indecisive expectations setting_mother positive tone", "legitimazinig expectation violation_mother positive tone", "v glorificaion feedback_mother positive tone", "v negative cr_mother positive tone", "v signal const_mother positive tone_control", "yes child independent clean up", "p motivational arrousal"]


def rollBehaviors(n):
    return list(itertools.combinations(behaviors, n))


def deleteInputAndOutpusFiles(iter):

    try:
        os.remove("C:\\TEMP\\mplus\\current"+str(iter)+".inp")
        os.remove("C:\\TEMP\\mplus\\current"+str(iter)+".out")
        print('deleted current'+str(iter))
    except Exception as e:
        print('failed to delete file ' + str(e))


def prepareInputFile(vars, iter):
    templateFileName = "C:\\TEMP\\mplus\\current_template.inp"
    input = ""
    with open(templateFileName, 'r') as f:
        strVars = str(vars)
        strVars = strVars.replace('(', '').replace(
            ')', '').replace("'", "").replace(",", ",\n")
        input = f.read().replace("[VARS_TEMPLATE]", strVars)
    text_file = open("C:\\TEMP\\mplus\\current"+str(iter)+".inp", "w+")
    n = text_file.write(input)
    text_file.close()


def runMplus(vars, iter):
    FNULL = open(os.devnull, 'w')
    filename = "C:\\TEMP\\mplus\\current"+str(iter)+".inp"
    fileDir = "C:\\TEMP\\mplus\\"

    # subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)
    try:

        # outputFile = open("C:\\TEMP\\mplus\\current"+str(iter)+".out", "w")
        # lock1 = threading.Lock()
        # lock1.acquire()

        outputFile = "C:\\TEMP\\mplus\\current"+str(iter)+".out"

        args = "C:\\TEMP\\mplus\\Mplus " + filename + " " + fileDir
        with open(outputFile, 'wb') as filehandle:
            # Popen(args.split(), stdout=outputFile, stderr=None)
            # filehandle.close()
            pipe = Popen(args.split(), stdout=PIPE, stderr=None)
            filehandle.write(pipe.communicate()[0])

        # stream = os.popen(args, stdout=outputFile)
        # outputFile = open("C:\\TEMP\\mplus\\current"+str(iter)+".out", "wb")
        # with open(outputFile, 'wb') as filehandle:
            # pipe = Popen(args.split(), stdout=None, stderr=None)
            # filehandle.write(pipe.communicate()[0])
        # output = stream.read()
        # n = text_file.write(output)
        # filehandle.close()
    except Exception as e:
        lock = threading.Lock()
        lock.acquire()
        try:
            errMsg = "failed vars: "+str(vars)+"\n"+"error:"+"\n"+str(e)
            print(errMsg)
            text_file = open("C:\\TEMP\\mplus\\errors.txt", "a")
            text_file.write(errMsg)
            text_file.close()
        finally:
            lock.release()  # release lock, no matter what
    # finally:
        # lock1.release()


def analyzeOutput(iter, offset, vars):
    filename = 'C:\\TEMP\\mplus\\current'+str(iter)+'.out'
    tableRow = line_num_for_phrase_in_file(0, filename)
    tableRow = line_num_for_phrase_in_file(tableRow, filename, "Classes")
    tableRow = line_num_for_phrase_in_file(tableRow, filename, "1")

    getLatentClassProbs(tableRow, iter, filename, vars)


def line_num_for_phrase_in_file(pos, filename, phrase='BASED ON THEIR MOST LIKELY LATENT CLASS MEMBERSHIP'):
    with open(filename, 'r') as f:
        for (i, line) in enumerate(f):
            if phrase in line:
                if i > pos:
                    return i
    return -1


def getLatentClassProbs(tableRow, iter, filename, vars):
    with open(filename, 'r') as f:
        all_lines_variable = f.readlines()
        c1 = getClassByLine(tableRow, all_lines_variable)
        # print(c1)
        maxClassRatio = c1['classRatio']
        minClassRatio = c1['classRatio']

        c2 = getClassByLine(tableRow+1, all_lines_variable)
        # print(c2)
        maxClassRatio = max(c2['classRatio'], maxClassRatio)
        minClassRatio = min(c2['classRatio'], minClassRatio)

        c3 = getClassByLine(tableRow+2, all_lines_variable)
        # print(c3)
        maxClassRatio = max(c3['classRatio'], maxClassRatio)
        minClassRatio = min(c3['classRatio'], minClassRatio)
    if ((c1['classRatio'] != c2['classRatio']) and ((c2['classRatio'] != c3['classRatio']))):
        if(keepOutput(maxClassRatio, minClassRatio, iter)):
            logOutput(c1['classRatio'], c2['classRatio'],
                      c3['classRatio'], filename, iter, vars)


def logOutput(c1, c2, c3, filename, iter, vars):
    with open("C:\\TEMP\\mplus\\mplusFilesLog.csv", "a", newline='') as text_file:
        writer = csv.writer(text_file)
        writer.writerow([iter, filename, str(vars), len(vars), c1, c2, c3])
    text_file.close()


def keepOutput(maxClassRatio, minClassRatio, iter):
    print('testing if to keep output')
    # if ((maxClassRatio < 86) or (minClassRatio > 10)):
    if (minClassRatio > 15):
        original = 'C:\\TEMP\\mplus\\current'+str(iter)+'.out'
        target = 'C:\\TEMP\\mplus\\\savedOutputs\\min15andup\\current' + \
            str(iter)+'.out'
        print('current'+str(iter)+'.out was saved')
        shutil.copyfile(original, target)
        return True
    else:
        if (minClassRatio > 13):
            original = 'C:\\TEMP\\mplus\\current'+str(iter)+'.out'
            target = 'C:\\TEMP\\mplus\\\savedOutputs\\min13andup\\current' + \
                str(iter)+'.out'
            print('current'+str(iter)+'.out was saved')
            shutil.copyfile(original, target)
            return True
        else:
            if (minClassRatio > 10):
                original = 'C:\\TEMP\\mplus\\current'+str(iter)+'.out'
                target = 'C:\\TEMP\\mplus\\\savedOutputs\\min10andup\\current' + \
                    str(iter)+'.out'
                print('current'+str(iter)+'.out was saved')
                shutil.copyfile(original, target)
                return True
    return False


def getClassByLine(rowNumber, all_lines_variable):
    line = all_lines_variable[rowNumber]
    content_array = line.split()
    lineClassObj = parseToClassArr(content_array)
    return lineClassObj


def parseToClassArr(arr):
    print(arr)
    classObj = {}
    classObj['classNum'] = int(arr[0])
    classObj['classRatio'] = int(arr[1])
    prob = (arr[2]).replace('\n', '')
    classObj['classProb'] = float(prob)
    print(classObj)
    return classObj
