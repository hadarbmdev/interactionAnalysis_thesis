import subprocess
import os
import math
import shutil
import itertools


behaviors = {"child_neutral_affect", "cleanup_not_requested", "mother_positive_affect", "no_child_independent_clean_up", "v_direct_concrete_inst", "p_touching_toys_for_cleanup", "v_small_mission_steps", "no_compliance_Passive", "p_signal_const", "yes_compliance", "v_positive_feedback", "p_positive_feedback", "v_signal_const", "v_perspective_mirroring", "p_mother_cleanup", "v_concern", "p_concern_exp", "child_positive_affect", "v_choice", "p_gentle_touch_for_clean_up", "v_rational", "p_affection_expression", "v_motivation_arousal", "v_unclear",
             "v_inadequate_perspective_invalidation", "v_action_oriented_feedback", "v_affection", "v_hostility", "no_compliance_Defiance", "p_modeling", "v_modeling", "p_forceful_touch_for_cleanup", "child_negative_affect", "no_compliance_Refusal", "child_alert", "no_inadequate_boundaries_setting", "indecisive_expectations_setting", "legitimazinig_expectation_violation", "v_glorificaion_feedback", "v_neg_cr", "yes_child_independent_clean_up", "v_threat_punishment", "p_motivational_arrousal", "child_tired", "v_material_reward", "v_negative_feedback", "unclear_compliance"}

behaviors1 = {"child_neutral_affect",
              "cleanup_not_requested", "mother_positive_affect"}


def rollBehaviors(n):
    return list(itertools.combinations(behaviors, n))


def prepareInputFile(vars):
    templateFileName = "C:\\TEMP\\mplus\\current_template.inp"
    input = ""
    with open(templateFileName, 'r') as f:
        strVars = str(vars)
        strVars = strVars.replace('(', '').replace(')', '').replace("'", "")
        input = f.read().replace("[VARS_TEMPLATE]", strVars)
    text_file = open("C:\\TEMP\\mplus\\current.inp", "w")
    n = text_file.write(input)
    text_file.close()


def runMplus():
    FNULL = open(os.devnull, 'w')
    filename = "C:\\TEMP\\mplus\\current.inp"
    fileDir = "C:\\TEMP\\mplus\\"
    args = "C:\\TEMP\\mplus\\Mplus " + filename + " " + fileDir
    #subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)

    stream = os.popen(args)
    output = stream.read()
    text_file = open("C:\\TEMP\\mplus\\current.out", "w")
    n = text_file.write(output)
    text_file.close()


def analyzeOutput(iter):
    tableRow = line_num_for_phrase_in_file()
    getLatentClassProbs(tableRow+4, iter)


def line_num_for_phrase_in_file(phrase='BASED ON THEIR MOST LIKELY LATENT CLASS MEMBERSHIP', filename='C:\\TEMP\\mplus\\current.out'):
    with open(filename, 'r') as f:
        for (i, line) in enumerate(f):
            if phrase in line:
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

    if ((maxClassRatio < 86) or (minClassRatio > 10)):
        original = 'C:\\TEMP\\mplus\\current.out'
        target = 'C:\\TEMP\\mplus\\\savedOutputs\\current'+str(iter)+'.out'
        print('current'+str(iter)+'.out was saved')
        shutil.copyfile(original, target)


def getClassByLine(rowNumber, all_lines_variable):
    line = all_lines_variable[rowNumber]
    content_array = line.split('          ')
    lineClassObj = parseToClassArr(content_array)
    return lineClassObj


def parseToClassArr(arr):
    classObj = {}
    classObj['classNum'] = int(arr[0])
    classObj['classRatio'] = int(arr[1])
    prob = (arr[2]).replace('\n', '')
    classObj['classProb'] = float(prob)
    return classObj
