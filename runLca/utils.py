from subprocess import Popen, PIPE, call, check_call
import fileinput
import os
import math
import shutil
import itertools
import threading
import csv
import pandas as pd

behaviors = ["vdirePT", "p_touchi", "vsmalpt", "p_signal", "vpsfdpt", "p_positi", "vsglpt", "vperspt", "vcncrpt", "p_concer", "v_choice", "p_gentle", "v_ration", "p_affect", "v_motiva", "pgenC", "v_inadeq",
             "v_action", "vafectpt", "vhostlpt", "p_modeli", "vmdlpt", "vdirptc", "csmlntc", "psgnC", "v_modeli", "vdirNTC", "vsmNTC", "p_forcef", "indecisi", "legitima", "v_glorif", "vngcrpt", "vsgnptc", "childInd", "p_motiva"]
children_behaviors = ["Cgilt", "Cconf",
                      "Cfix", "Ccomp", "Cemp", "Cext", "Cint"]
behaviors_extended = ["v direct concrete inst_mother positive tone", "p touching toys for cleanup", "v small mission steps_mother positive tone", "p signal const", "v positive feedback_mother positive tone", "p positive feedback", "v signal const_mother positive tone", "v perspective/mirroring_mother positive tone", "v concern_mother positive tone", "p concern exp", "v choice_mother positive tone", "p gentle touch for clean up", "v rational_mother positive tone", "p affection expression", "v motivation arousal_mother positive tone", "p gentle touch for clean up_control", "v inadequate perspective/invalidation_mother positive tone", "v action oriented feedback_mother positive tone", "v affection_mother positive tone",
                      "v hostility_mother positive tone", "p modeling", "v modeling_mother positive tone", "v direct concrete inst_mother positive tone_control", "v small mission steps_mother negative tone_control", "p signal const_control", "v modeling_mother negative tone", "v direct concrete inst_mother negative tone_control", "v small mission steps_mother positive tone_control", "p forceful touch for cleanup", "indecisive expectations setting_mother positive tone", "legitimazinig expectation violation_mother positive tone", "v glorificaion feedback_mother positive tone", "v negative cr_mother positive tone", "v signal const_mother positive tone_control", "yes child independent clean up", "p motivational arrousal"]
subjects = ['subjects_011', 'subjects_012', 'subjects_015', 'subjects_016', 'subjects_018', 'subjects_020', 'subjects_021', 'subjects_022', 'subjects_023', 'subjects_026', 'subjects_028', 'subjects_029', 'subjects_030', 'subjects_031', 'subjects_032', 'subjects_034', 'subjects_036', 'subjects_037', 'subjects_038', 'subjects_039', 'subjects_041', 'subjects_043', 'subjects_044', 'subjects_048', 'subjects_050', 'subjects_057', 'subjects_059', 'subjects_063', 'subjects_066', 'subjects_067', 'subjects_069', 'subjects_070', 'subjects_082', 'subjects_083', 'subjects_085', 'subjects_100', 'subjects_105', 'subjects_109', 'subjects_113', 'subjects_118', 'subjects_119', 'subjects_121', 'subjects_126', 'subjects_132', 'subjects_133', 'subjects_148', 'subjects_149', 'subjects_152', 'subjects_161', 'subjects_166', 'subjects_169',
            'subjects_170', 'subjects_177', 'subjects_178', 'subjects_180', 'subjects_181', 'subjects_186', 'subjects_191', 'subjects_199', 'subjects_203', 'subjects_204', 'subjects_209', 'subjects_210', 'subjects_211', 'subjects_214', 'subjects_215', 'subjects_217', 'subjects_219', 'subjects_225', 'subjects_226', 'subjects_227', 'subjects_236', 'subjects_238', 'subjects_239', 'subjects_240', 'subjects_244', 'subjects_250', 'subjects_251', 'subjects_254', 'subjects_256', 'subjects_258', 'subjects_262', 'subjects_263', 'subjects_267', 'subjects_272', 'subjects_273', 'subjects_277', 'subjects_282', 'subjects_283', 'subjects_284', 'subjects_285', 'subjects_286', 'subjects_292', 'subjects_293', 'subjects_294', 'subjects_297', 'subjects_299', 'subjects_304', 'subjects_306', 'subjects_307', 'subjects_309']

children_subjects = ['subjects_012', 'subjects_015', 'subjects_016', 'subjects_020', 'subjects_021', 'subjects_026', 'subjects_028', 'subjects_029', 'subjects_030', 'subjects_037', 'subjects_038', 'subjects_039', 'subjects_041', 'subjects_043', 'subjects_044', 'subjects_050', 'subjects_057', 'subjects_059', 'subjects_063', 'subjects_067', 'subjects_082', 'subjects_083', 'subjects_085', 'subjects_100', 'subjects_109', 'subjects_113', 'subjects_177', 'subjects_178', 'subjects_180', 'subjects_191', 'subjects_203', 'subjects_209', 'subjects_210', 'subjects_214', 'subjects_217', 'subjects_219', 'subjects_225', 'subjects_226', 'subjects_236', 'subjects_238', 'subjects_240', 'subjects_258', 'subjects_262', 'subjects_263', 'subjects_277', 'subjects_282', 'subjects_283', 'subjects_284', 'subjects_285', 'subjects_292', 'subjects_294', 'subjects_297', 'subjects_299', 'subjects_304', 'subjects_306', 'subjects_307', 'subjects_309'
                     ]


def rollBehaviors(n, sentBehaviors):
    return list(itertools.combinations(sentBehaviors, n))


def NoEmptyObservations(gelemDf, lcaVars):

    for idx, observation in gelemDf.iterrows():
        # print(idx, observation)
        observationName = gelemDf.loc[idx, "subjects"]
        print('Checking observation ' +
              str(observationName) + " for vars "+str(lcaVars))
        isObservationEmptyOnAllVars = True
        # print(idx)

        for lcaVar in lcaVars:
            observationValue = gelemDf.loc[idx, lcaVar]
            # print('observationValue='+str(observationValue))
            if (observationValue != 99999):
                isObservationEmptyOnAllVars = False
                # print('observation '+str(observationName +
                #  " is NOT empty on all these vars "+str(lcaVars)))
        if(isObservationEmptyOnAllVars):
            print('observation '+str(observationName +
                                     " is EMPTY on all these vars "+str(lcaVars)))
            return False
    print('no empty observations found for vars '+str(lcaVars))
    return True


def getSubjectsArrNames():
    gelemInput = pd.read_csv('C:\\TEMP\\mplus\\selectedBehaviors_gelem.dat')
    for index, row in gelemInput.iterrows():
        subjectName = row[0]
        subjects.append(subjectName)
    print(subjects)


# def rollBehaviors(n):
#     return list(itertools.combinations(behaviors, n))


def deleteInputAndOutpusFiles(iter, filePrefix):

    try:
        os.remove("C:\\TEMP\\mplus\\current"+filePrefix+str(iter)+".inp")
        os.remove("C:\\TEMP\\mplus\\current"+filePrefix+str(iter)+".out")
        os.remove("C:\\TEMP\\mplus\\lca1_save_"+str(iter)+".txt")
        os.remove("C:\\TEMP\\mplus\\lca1_save_"+str(iter)+".csv")
        os.remove("C:\\TEMP\\mplus\\lca1_save_"+str(iter)+".txt_copy")

        print('deleted current'+str(iter))
    except Exception as e:
        print('failed to delete file ' + str(e))


def prepareInputFile(vars, iter, templateFileName, filePrefix):
    # templateFileName = "C:\\TEMP\\mplus\\current_template.inp"
    input = ""
    with open(templateFileName, 'r') as f:
        strVars = str(vars)
        strVars = strVars.replace('(', '').replace(
            ')', '').replace("'", "").replace(",", ",\n")
        input = f.read().replace("[VARS_TEMPLATE]", strVars)
    text_file = open("C:\\TEMP\\mplus\\current" +
                     filePrefix+str(iter)+".inp", "w+")
    n = text_file.write(input)
    text_file.close()


def prepareInputFileWithName(vars, iter, templateFileName, filePrefix):
    # templateFileName = "C:\\TEMP\\mplus\\current_template.inp"
    input = ""
    with open(templateFileName, 'r') as f:
        strVars = str(vars)
        strVars = strVars.replace('(', '').replace(
            ')', '').replace("'", "").replace(",", ",\n")
        input = f.read().replace("[VARS_TEMPLATE]", strVars).replace(
            "[NAME_TEMPLATE]", str(iter))
    text_file = open("C:\\TEMP\\mplus\\current" +
                     filePrefix+str(iter)+".inp", "w+")
    print(" Created input file: C:\\TEMP\\mplus\\current" +
          filePrefix+str(iter)+".inp")
    n = text_file.write(input)
    text_file.close()


def runMplusWithSaveFile(vars, iter, filePrefix):
    FNULL = open(os.devnull, 'w')
    filename = "C:\\TEMP\\mplus\\current"+filePrefix+str(iter)+".inp"
    fileDir = "C:\\TEMP\\mplus\\"

    # subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)
    try:

        # outputFile = open("C:\\TEMP\\mplus\\current"+str(iter)+".out", "w")
        # lock1 = threading.Lock()
        # lock1.acquire()

        outputFile = "C:\\TEMP\\mplus\\current"+filePrefix+str(iter)+".out"

        args = "C:\\TEMP\\mplus\\Mplus " + filename + " " + fileDir
        print(args)
        # with open(outputFile, 'wb') as filehandle:

        process = Popen(args.split(), stdout=PIPE, stderr=None)
        stdout, stderr = process.communicate()

        os.popen(args)

        # filehandle.close()
        # pipe = Popen(args.split(), stdout=PIPE, stderr=None)
        # filehandle.write(pipe.communicate()[0])

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
            errMsg = "Failed to run mplus. failed vars: " + \
                str(vars)+"\n"+"error: "+"\n"+str(e)
            # print(errMsg)
            text_file = open("C:\\TEMP\\mplus\\errors.txt", "a")
            text_file.write(errMsg)
            text_file.close()
        finally:
            lock.release()  # release lock, no matter what
            print('finished running mplus on: '+str(vars))
    # finally:
        # lock1.release()


def runMplus(vars, iter, filePrefix):
    FNULL = open(os.devnull, 'w')
    filename = "C:\\TEMP\\mplus\\current"+filePrefix+str(iter)+".inp"
    fileDir = "C:\\TEMP\\mplus\\"

    # subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)
    try:

        # outputFile = open("C:\\TEMP\\mplus\\current"+str(iter)+".out", "w")
        # lock1 = threading.Lock()
        # lock1.acquire()

        outputFile = "C:\\TEMP\\mplus\\current"+filePrefix+str(iter)+".out"

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
            errMsg = "Failed to run mplus. failed vars: " + \
                str(vars)+"\n"+"error: "+"\n"+str(e)
            print(errMsg)
            text_file = open("C:\\TEMP\\mplus\\errors.txt", "a")
            text_file.write(errMsg)
            text_file.close()
        finally:
            lock.release()  # release lock, no matter what
            print('finished running mplus on: '+str(vars))
    # finally:
        # lock1.release()


def analyzeOutput(iter, offset, vars, filePrefix, sMin, sAvg, sMax, splitVars):
    filename = 'C:\\TEMP\\mplus\\current'+filePrefix+str(iter)+'.out'
    tableRow = line_num_for_phrase_in_file(0, filename)
    tableRow = line_num_for_phrase_in_file(tableRow, filename, "Classes")
    tableRow = line_num_for_phrase_in_file(tableRow, filename, "1")

    getLatentClassProbs(tableRow, iter, filename, vars,
                        filePrefix, sMin, sAvg, sMax, splitVars)


def getEachVarMeanPerGroup(iter, vars, filePrefix, splitVars):
    outputFile = "C:\\TEMP\\mplus\\current"+filePrefix+str(iter)+".out"
    tableRow = line_num_for_phrase_in_file(0, outputFile, "MODEL RESULTS")

    means = {"v1Mean": {}, "v2Mean": {}, "v3Mean": {}}
    with open(outputFile, 'r') as f:
        all_lines_variable = f.readlines()

        # go to C1 means of all vars.
        tableRow = line_num_for_phrase_in_file(line_num_for_phrase_in_file(
            0, outputFile, "Latent Class 1"), outputFile, "Means")
        tableRow = tableRow + 1
        means["v1Mean"] = getMeansByLine(tableRow, all_lines_variable)

        # go to C2 means of all vars.
        tableRow = line_num_for_phrase_in_file(line_num_for_phrase_in_file(
            0, outputFile, "Latent Class 2"), outputFile, "Means")
        tableRow = tableRow + 1
        means["v2Mean"] = getMeansByLine(tableRow, all_lines_variable)

        # go to C3 means of all vars.
        tableRow = line_num_for_phrase_in_file(line_num_for_phrase_in_file(
            0, outputFile, "Latent Class 3"), outputFile, "Means")
        tableRow = tableRow + 1
        means["v3Mean"] = getMeansByLine(tableRow, all_lines_variable)
    return means


def analyzeOutputToGetMothersOfEachSubjectLCAGroup(iter, offset, vars, filePrefix, splitVars):
    # filename = 'C:\\TEMP\\mplus\\lca1_save_'+str(iter)+'.txt'
    filename = 'C:\\TEMP\\mplus\\lca1_save_'+str(iter)+'.txt'
    dst = 'C:\\TEMP\\mplus\\lca1_save_'+str(iter)+'.csv'
    convertOutputResultsFileToCsv(filename, dst, len(splitVars))
    resultsFileName = 'C:\\TEMP\\mplus\\' + \
        filePrefix.replace('_', "")+'LCAresults.csv'
    copySubjectsLCAtoCSV(dst, iter, resultsFileName, vars, filePrefix)
    # tableRow = line_num_for_phrase_in_file(0, filename)
    # tableRow = line_num_for_phrase_in_file(tableRow, filename, "Classes")
    # tableRow = line_num_for_phrase_in_file(tableRow, filename, "1")

    # getLatentClassProbs(tableRow, iter, filename, vars)


def copySubjectsLCAtoCSV(dst, iter, resultsFileName, vars, filePrefix):

    dfCurrentResult = pd.read_csv(dst)
    # print("dfCurrentResult = " + str(dfCurrentResult.iloc[0]))
    dfResults = pd.read_csv(resultsFileName)
    # print(dfResults)
    newColName = vars.replace(",", "_")
    subjectsWithDataIndex = 0

    newResultsCol = []

    if "children" in filePrefix:
        subjectsToExamine = children_subjects
    else:
        subjectsToExamine = subjects
    for rowIndex, row in dfResults.iterrows():
        # print("rowIndex "+str(rowIndex))
        subjectIndex = ""
        if (rowIndex + 10 < 100):
            subjectIndex = "0" + str(row["ID"])
        else:
            subjectIndex = row["ID"]
        subjectsId = "subjects_" + str(subjectIndex).replace(".0", "")
        # print('subjectsId = '+str(subjectsId))
        # print('subjectsWithDataIndex = '+str(subjectsWithDataIndex))
        # print('subjects[subjectsWithDataIndex] = ' +
        #   str(subjects[subjectsWithDataIndex]))

        if (subjectsId == subjectsToExamine[subjectsWithDataIndex]):
            resultRow = dfCurrentResult.iloc[subjectsWithDataIndex]
            # print(resultRow)
            # print('subjectsWithDataIndex ' + str(subjectsWithDataIndex))
            subjectGroup = dfCurrentResult.iloc[subjectsWithDataIndex, -1]
            subjectsWithDataIndex = subjectsWithDataIndex + 1
            # print(str(subjectsId) + ":  " + str(subjectGroup))
            newResultsCol.append(subjectGroup)
        else:
            # print(str(subjectsId) + ":  0")
            newResultsCol.append(0)

    # print("newResultsCol " + str(newResultsCol) +
        #   " length: "+str(len(newResultsCol)))
    dfResults[newColName] = newResultsCol
    dfResults = addMeansResultsOfCurrentVarsForThisSubject(dfResults, vars)
    # print(dfResults)
    dfResults.to_csv(resultsFileName, index=False)
    return 1


def addMeansResultsOfCurrentVarsForThisSubject(dfResults, vars):
    amountOfVars = len(vars.split(","))


def convertOutputResultsFileToCsv(filename, dst, noOfVars):

    shutil.copyfile(filename, filename+'_copy')
    title = ""
    for v in range(noOfVars+3):
        title = title + "v" + str(v+1) + ","
    title = title + "class \n"
    print("title "+title)
    with open(dst, 'w') as newfile:
        newfile.write(title)
        for line in open(filename+'_copy', 'r'):
            newline = line.replace('      ', ',')
            newline = newline.replace(',   *,', '   *,')
            print(newline)
            newfile.write(newline)
    # newfile.close()
    # filename.close()

    # with open(dst, "r+", newline='') as text_file:
    #     writer = csv.writer(text_file)
    #     writer.writerow(["v1", "v2", "v3",
    #                     "v4", "v5", "v6", "class"])
    # text_file.close()


def line_num_for_phrase_in_file(pos, filename, phrase='BASED ON THEIR MOST LIKELY LATENT CLASS MEMBERSHIP'):
    with open(filename, 'r') as f:
        for (i, line) in enumerate(f):
            if phrase in line:
                if i > pos:
                    return i
    return -1


def getLatentClassProbs(tableRow, iter, filename, vars, filePrefix, sMin, sAvg, sMax, splitVars):

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

        print('minClassRatio '+str(minClassRatio))
    if ((c1['classRatio'] != c2['classRatio']) and ((c2['classRatio'] != c3['classRatio']))):
        if(keepOutput(maxClassRatio, minClassRatio, iter, filePrefix, sMin, sAvg, sMax)):
            varMeansPerGroup = getEachVarMeanPerGroup(
                iter, vars, filePrefix, splitVars)
            logOutput(c1['classRatio'], c2['classRatio'],
                      c3['classRatio'], filename, iter, vars, varMeansPerGroup, filePrefix)

            return varMeansPerGroup


def logOutput(c1, c2, c3, filename, iter, vars, varMeansPerGroup, filePrefix):
    with open("C:\\TEMP\\mplus\\mplusFilesLog"+filePrefix+".csv", "a", newline='') as text_file:
        writer = csv.writer(text_file)
        writer.writerow([iter, filename, str(vars), len(
            vars), c1, c2, c3, str(varMeansPerGroup)])
    text_file.close()


def keepOutput(maxClassRatio, minClassRatio, iter, filePrefix, sMin, sAvg, sMax):
    print('testing if to keep output')
    # if ((maxClassRatio < 86) or (minClassRatio > 10)):
    os.makedirs(os.path.dirname(
        'C:\\TEMP\\mplus\\savedOutputs\\min'+str(sMax)), exist_ok=True)
    os.makedirs(os.path.dirname(
        'C:\\TEMP\\mplus\\savedOutputs\\min'+str(sAvg)), exist_ok=True)
    os.makedirs(os.path.dirname(
        'C:\\TEMP\\mplus\\savedOutputs\\min'+str(sMin)), exist_ok=True)
    if (minClassRatio > sMax):
        original = 'C:\\TEMP\\mplus\\current'+filePrefix+str(iter)+'.out'
        target = 'C:\\TEMP\\mplus\\savedOutputs\\min'+str(sMax)+'andup\\current'+filePrefix + \
            str(iter)+'.out'
        print('current'+filePrefix+str(iter)+'.out was saved')
        shutil.copyfile(original, target)
        print('YES, KEEP')
        return True
    else:
        if (minClassRatio > sAvg):
            original = 'C:\\TEMP\\mplus\\current'+filePrefix+str(iter)+'.out'
            target = 'C:\\TEMP\\mplus\\savedOutputs\\min'+str(sAvg)+'andup\\current'+filePrefix + \
                str(iter)+'.out'
            print('current'+str(iter)+'.out was saved')
            shutil.copyfile(original, target)
            print('YES, KEEP')
            return True
        else:
            if (minClassRatio > sMin):
                original = 'C:\\TEMP\\mplus\\current' + \
                    filePrefix+str(iter)+'.out'
                target = 'C:\\TEMP\\mplus\\savedOutputs\\min'+str(sMin)+'andup\\current' + filePrefix + \
                    str(iter)+'.out'
                print('current'+str(iter)+'.out was saved')
                shutil.copyfile(original, target)
                print('YES, KEEP')
                return True
    print('NO, DISCARD')
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


def getMeansByLine(rowNumber, all_lines_variable):
    allVarsMeansArr = []
    for i in range(3):
        line = all_lines_variable[rowNumber+i]
        content_array = line.split()
        lineClassObj = parseToMeanArr(content_array)
        allVarsMeansArr.append(lineClassObj)
    # print("allVarsMeansArr " + str(allVarsMeansArr))
    return allVarsMeansArr


def parseToMeanArr(arr):
    print(arr)
    classObj = {}
    classObj[arr[0]] = float(arr[1])
    # print("parseToMeanArr: " + str(classObj))
    return classObj
