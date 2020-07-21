import subprocess
import os
import math
import shutil
import itertools
import threading


behaviors = {"child_neutral_affect", "cleanup_not_requested", "mother_positive_affect", "no_child_independent_clean_up", "v_direct_concrete_inst", "p_touching_toys_for_cleanup", "v_small_mission_steps", "no_compliance_Passive", "p_signal_const", "yes_compliance", "v_positive_feedback", "p_positive_feedback", "v_signal_const", "v_perspective_mirroring", "p_mother_cleanup", "v_concern", "p_concern_exp", "child_positive_affect", "v_choice", "p_gentle_touch_for_clean_up", "v_rational", "p_affection_expression", "v_motivation_arousal",
             "v_inadequate_perspective_invalidation", "v_action_oriented_feedback", "v_affection", "v_hostility", "no_compliance_Defiance", "p_modeling", "v_modeling", "p_forceful_touch_for_cleanup", "child_negative_affect", "no_compliance_Refusal", "child_alert", "indecisive_expectations_setting", "legitimazinig_expectation_violation", "v_glorificaion_feedback", "v_neg_cr", "yes_child_independent_clean_up", "v_threat_punishment", "p_motivational_arrousal", "child_tired", "v_material_reward", "v_negative_feedback"}

behaviors1 = {"child_neutral_affect",
              "cleanup_not_requested", "mother_positive_affect"}


def rollBehaviors(n):
    return list(itertools.combinations(behaviors, n))

def deleteInputAndOutpusFiles(iter):
    try:
        os.remove("C:\\TEMP\\mplus\\current"+str(iter)+".inp")
        os.remove("C:\\TEMP\\mplus\\current"+str(iter)+".out")
    except Exception as e:
        print('failed to delete file '+ str(e))

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
    args = "C:\\TEMP\\mplus\\Mplus " + filename + " " + fileDir
    # subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)
    try:
        # print('STARTING to run mplus of iteration '+str(iter))
        stream = os.popen(args)
        output = stream.read()
        # print('FINISHED to run mplus of iteration '+str(iter))
        text_file = open("C:\\TEMP\\mplus\\current"+str(iter)+".out", "w")
        n = text_file.write(output)
        text_file.close()
    except Exception as e:
        lock = threading.Lock()
        lock.acquire()
        try:
            text_file = open("C:\\TEMP\\mplus\\errors.txt", "w")
            text_file.write(
                "failed vars: "+str(vars)+"\n"+"error:"+"\n"+str(e))
            text_file.close()
        finally:
            lock.release() # release lock, no matter what


def analyzeOutput(iter, offset):
    tableRow = line_num_for_phrase_in_file(0)
    tableRow = line_num_for_phrase_in_file(tableRow, "Classes")
    tableRow = line_num_for_phrase_in_file(tableRow, "1")
    getLatentClassProbs(tableRow, iter)


def line_num_for_phrase_in_file(pos, phrase='BASED ON ESTIMATED POSTERIOR PROBABILITIES', filename='C:\\TEMP\\mplus\\current.out'):
    with open(filename, 'r') as f:
        for (i, line) in enumerate(f):
            if phrase in line:
                if i > pos:
                    return i
    return -1


def getLatentClassProbs(tableRow, iter, filename='C:\\TEMP\\mplus\\current.out', ):
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
        keepOutput(maxClassRatio, minClassRatio, iter)


def keepOutput(maxClassRatio, minClassRatio, iter):

    # if ((maxClassRatio < 86) or (minClassRatio > 10)):
    if (minClassRatio > 15):
        original = 'C:\\TEMP\\mplus\\current.out'
        target = 'C:\\TEMP\\mplus\\\savedOutputs\\15andup\\current' + \
            str(iter)+'.out'
        print('current'+str(iter)+'.out was saved')
        shutil.copyfile(original, target)
    else:
        if (minClassRatio > 9):
            original = 'C:\\TEMP\\mplus\\current.out'
            target = 'C:\\TEMP\\mplus\\\savedOutputs\\9andup\\current' + \
                str(iter)+'.out'
            print('current'+str(iter)+'.out was saved')
            shutil.copyfile(original, target)

        else:
            if (maxClassRatio < 83):
                original = 'C:\\TEMP\\mplus\\current.out'
                target = 'C:\\TEMP\\mplus\\\savedOutputs\\83anddown\\current' + \
                    str(iter)+'.out'
                print('current'+str(iter)+'.out was saved')
                shutil.copyfile(original, target)


def getClassByLine(rowNumber, all_lines_variable):
    line = all_lines_variable[rowNumber]
    content_array = line.split()
    lineClassObj = parseToClassArr(content_array)
    return lineClassObj


def parseToClassArr(arr):
    print(arr)
    classObj = {}
    classObj['classNum'] = int(arr[0])
    classObj['classRatio'] = float(arr[1])
    prob = (arr[2]).replace('\n', '')
    classObj['classProb'] = float(prob)
    print(classObj)
    return classObj
