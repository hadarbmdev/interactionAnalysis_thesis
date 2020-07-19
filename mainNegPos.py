from utils import drawSubPlotForMotherAndChild, operateOnJsonFiles, setCodeEntry, setBehaviorAndEmotionEntry, prepareCsvForSubject, replaceComma, getParticipantsCode, convertLegendCsvToJson
LIMIT = 9  # 309


def main():
    operateOnJsonFiles(replaceComma, 'replaceComma', 'jsonsPosNeg//', '')
    operateOnJsonFiles(setBehaviorAndEmotionEntry,
                       "setBehaviorEntry", 'jsonsPosNeg//',  '')
    operateOnJsonFiles(replaceComma, 'replaceComma', 'jsonsPosNeg//', '')
    # operateOnJsonFiles(replaceComma, 'replaceComma', 'jsons//')
    # operateOnJsonFiles(setCodeEntry, "setCodeEntry", 'jsons//')
    # operateOnJsonFiles(replaceComma, 'replaceComma', 'jsons//')
    # operateOnJsonFiles(prepareCsvForSubject, 'prepareCsvForSubject', 'jsons//')
    # operateOnJsonFiles(replaceComma, 'replaceComma', 'output//')
    # codes = getParticipantsCode("none")
    # drawSubPlotForMotherAndChild("output//", codes, LIMIT)


main()
