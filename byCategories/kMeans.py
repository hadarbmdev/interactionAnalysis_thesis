from utils import convertLegendCsvToJson, loadCsvForSubject, operateOnJsonObjAcrossAllJsonFiles, operateOnJsonFiles, operateOnJsonFilesForMatrix, createCodeRepresenation, get_key, swapBehaviorAndCodes, getKeyForValue
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import json
from operator import itemgetter
import os
import fileinput
import matplotlib.pyplot as plt
from pandas import plotting
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import plotly
import plotly.graph_objs as go


subjectsbehaviors = ["child neutral affect", "cleanup not requested", "mother positive affect", "no child independent clean up", "v direct concrete inst", "p touching toys for cleanup", "v small mission steps", "no compliance - Passive", "p signal const", "yes compliance", "v positive feedback", "p positive feedback", "v signal const", "v perspective/mirroring", "p mother cleanup", "v concern", "p concern exp", "child positive affect", "v choice", "p gentle touch for clean up", "v rational", "p affection expression", "v motivation arousal", "v unclear",
                     "v inadequate perspective/invalidation", "v action oriented feedback", "v affection", "v hostility", "no compliance - Defiance", "p modeling", "v modeling", "p forceful touch for cleanup", "child negative affect", "no compliance - Refusal", "child alert", "no inadequate boundaries setting", "indecisive expectations setting", "legitimazinig expectation violation", "v glorificaion feedback", "v negative cr", "yes child independent clean up", "v threat punishment", "p motivational arrousal", "child tired", "v material reward", "v negative feedback", "unclear compiance"]


def cluster_kmeans(subject):

    df = pd.read_csv('behaviorsCodesAndFrequencyRatio_' +
                     subject+'.csv', usecols=swapBehaviorAndCodes().values())
    # print(df)
    clustering_kmeans = KMeans(
        n_clusters=5, precompute_distances="auto", n_jobs=-1)
    df['clusters'] = clustering_kmeans.fit_predict(df)
    df.to_csv('clusters_'+subject+'.csv')
    # Run PCA on the data and reduce the dimensions in pca_num_components dimensions
    # pca_num_components = 2
    # reduced_data = PCA(n_components=pca_num_components).fit_transform(df)
    # results = pd.DataFrame(reduced_data, columns=['pca1', 'pca2'])

    # sns.scatterplot(x="pca1", y="pca2", hue=df['clusters'], data=results)
    # plt.title('K-means Clustering with 2 dimensions')
    # plt.show()
    print(df['clusters'])
    grouped = df.groupby(['clusters'], sort=True)
    print('grouped:'+str(grouped))
    # compute sums for every column in every group
    sums = grouped.sum()
    print('sums:'+str(sums))
    dfCols = pd.read_csv('behaviorsCodesAndFrequencyRatio_' +
                         subject+'.csv', usecols=["subjectCode"])

    cols = []
    for index, row in dfCols.iterrows():
        cols.append(row['subjectCode'])
    # print(cols)
    pivotted = df.pivot(cols, subjectsbehaviors, sums.values.tolist())

    sns.heatmap(pivotted, cmap='RdBu')


def cluster_kmeans_jupiter(subject):
    plotly.offline.init_notebook_mode()
    df = pd.read_csv('behaviorsCodesAndFrequencyRatio_' +
                     subject+'.csv', usecols=swapBehaviorAndCodes().values())
    # print(df)
    clustering_kmeans = KMeans(
        n_clusters=7, precompute_distances="auto", n_jobs=-1)
    df['clusters'] = clustering_kmeans.fit_predict(df)
    df.to_csv('clusters_'+subject+'.csv')
    # Run PCA on the data and reduce the dimensions in pca_num_components dimensions
    # pca_num_components = 2
    # reduced_data = PCA(n_components=pca_num_components).fit_transform(df)
    # results = pd.DataFrame(reduced_data, columns=['pca1', 'pca2'])

    # sns.scatterplot(x="pca1", y="pca2", hue=df['clusters'], data=results)
    # plt.title('K-means Clustering with 2 dimensions')
    # plt.show()
    print(df['clusters'])
    grouped = df.groupby(['clusters'], sort=True)
    print('grouped:'+str(grouped))
    # compute sums for every column in every group
    sums = grouped.sum()
    print('sums:'+str(sums))
    dfCols = pd.read_csv('behaviorsCodesAndFrequencyRatio_' +
                         subject+'.csv', usecols=["subjectCode"])

    cols = []
    for index, row in dfCols.iterrows():
        cols.append(row['subjectCode'])
    # print(cols)
    data = [go.Heatmap(z=sums.values.tolist(),
                       y=[cols],
                       x=[subjectsbehaviors],
                       colorscale='Viridis')]

    plotly.offline.iplot(data, filename='pandas-heatmap')


def rename_columns(df, prefix='x'):
    """
    Rename the columns of a dataframe to have X in front of them

    :param df: data frame we're operating on
    :param prefix: the prefix string
    """
    df = df.copy()
    df.columns = [prefix + str(i) for i in df.columns]
    return df


def prepareDf4SubjectWithBehaviorCodes(subject):
    df = pd.read_csv('behaviorFrequencyByTurnRatio_' +
                     subject+'.csv')
    newNames = swapBehaviorAndCodes()
    df = df.rename(columns=newNames)
    df.to_csv('behaviorsCodesAndFrequencyRatio_' +
              subject+'.csv')
    print(df)


def getBehaviorsGroup():
    legendFile = open('legend.json')
    legend = json.load(legendFile)
    behaviorsGroup = set(legend["Behavior Group"].values())
    print(behaviorsGroup)
    return behaviorsGroup


def mapBehaviorNameTo(subjectTurn, to):
    legendFile = open('legend.json')
    legend = json.load(legendFile)

    legendColumnX = "Behavior"
    lookupValue = subjectTurn["Behavior"]
    legendSubTableX = legend[legendColumnX]
    xKey = getKeyForValue(legendSubTableX, lookupValue)
    if (xKey != "-1"):
        legendColumnY = to
        # print('looking up in table "' + str(legendColumnY) +'" at key ' + str(xKey))

        legendSubTableY = legend[legendColumnY]
        targetValueY = legendSubTableY[xKey]
        # print('... found: ' + str(targetValueY))

        if (not "Code" in subjectTurn):
            subjectTurn["Code"] = -1
        subjectTurn["Code"] = targetValueY
    else:
        print('did not find key for lookupValue: "' +
              (lookupValue) + '" on column ' + legendColumnX)

    return subjectTurn


def convertToFrequencyRatioBySubject(subject):
    print('convertToFrequencyRatioBySubject')
    dir = 'jsons//'
    directory = os.fsencode(dir)
    allInteractions = {}

    outputFile = open('behaviorFrequencyByTurnRatio_' +
                      subject+'.csv', 'w', newline='')  # load csv file
    output = csv.writer(outputFile)  # create a csv.write

    output.writerow(['subjectCode']+subjectsbehaviors)  # header row

    for file in os.listdir(directory):

        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            print('operating on ' + filename)

            interactionFile = open(dir + filename)
            turnsArray = json.load(interactionFile)
            allSubjectBehaviorsCountPerInteraction = {}
            subjectCode = filename.replace('.json', '')

            subjectTurnsArr = [
                x for x in turnsArray if x['Subject'] == subject]
            subjectTurnsCount = len(subjectTurnsArr)

            for behavior in subjectsbehaviors:
                allSubjectBehaviorsCountPerInteraction[behavior] = 0

            for subjectTurn in subjectTurnsArr:  # count number of behaviors across all turns of this subject
                turnBehavior = subjectTurn['Behavior']
                allSubjectBehaviorsCountPerInteraction[
                    turnBehavior] = allSubjectBehaviorsCountPerInteraction[turnBehavior] + 1

            for behavior in subjectsbehaviors:  # divide each behavior count in total turns count
                allSubjectBehaviorsCountPerInteraction[
                    behavior] = allSubjectBehaviorsCountPerInteraction[behavior] / subjectTurnsCount

            csvRow = [subjectCode] + \
                list(allSubjectBehaviorsCountPerInteraction.values())

            output.writerow(csvRow)  # values row
            # print(allSubjectBehaviorsCountPerInteraction)
            allInteractions[subjectCode] = allSubjectBehaviorsCountPerInteraction
            # print('allInteractions: '+str(allInteractions))

        else:
            continue

    # print("allInteractions: ")
    # print(allInteractions)

    return allInteractions


def convertToFrequencyRatioBySubjectCategory(subject):
    print('convertToFrequencyRatioBySubjectCategory')
    dir = 'jsons//'
    directory = os.fsencode(dir)
    allInteractions = {}

    outputFile = open('behaviorCategoryFrequencyByTurnRatio_' +
                      subject+'.csv', 'w', newline='')  # load csv file
    output = csv.writer(outputFile)  # create a csv.write
    headers = list(getBehaviorsGroup())
    headers.insert(0, 'subjectCode')
    print(headers)
    output.writerow(headers)  # header row

    for file in os.listdir(directory):

        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            print('operating on ' + filename)

            interactionFile = open(dir + filename)
            interactionFile = open(dir + filename)
            turnsArray = json.load(interactionFile)
            allSubjectBehaviorsCountPerInteraction = {}
            subjectCode = filename.replace('.json', '')

            subjectTurnsArr = [
                x for x in turnsArray if x['Subject'] == subject]
            subjectTurnsCount = len(subjectTurnsArr)

            for subjectTurn in subjectTurnsArr:  # count number of behaviors across all turns of this subject
                subjectTurn = mapBehaviorNameTo(subjectTurn, "Behavior Group")
                turnBehavior = subjectTurn['Code']
                if (turnBehavior not in allSubjectBehaviorsCountPerInteraction):
                    allSubjectBehaviorsCountPerInteraction[turnBehavior] = 0
                allSubjectBehaviorsCountPerInteraction[
                    turnBehavior] = allSubjectBehaviorsCountPerInteraction[turnBehavior] + 1

            # divide each behavior count in total turns count
            for behavior in allSubjectBehaviorsCountPerInteraction.keys():
                allSubjectBehaviorsCountPerInteraction[
                    behavior] = allSubjectBehaviorsCountPerInteraction[behavior] / subjectTurnsCount

            headersValues = list()  # always the first element
            headersValues.insert(0, subjectCode)
            for header in headers:  # create a row sorted as the headers are sorted
                if (header != 'subjectCode'):
                    if (header not in allSubjectBehaviorsCountPerInteraction):
                        allSubjectBehaviorsCountPerInteraction[header] = 0
                    headersValues.append(
                        allSubjectBehaviorsCountPerInteraction[header])

            output.writerow(headersValues)  # values row
            # print(allSubjectBehaviorsCountPerInteraction)
            allInteractions[subjectCode] = allSubjectBehaviorsCountPerInteraction
            # print('allInteractions: '+str(allInteractions))

        else:
            continue

    # print("allInteractions: ")
    # print(allInteractions)

    return allInteractions


# convertToFrequencyRatioBySubject('mother')
# convertToFrequencyRatioBySubject('child')
# prepareDf4SubjectWithBehaviorCodes('mother')
# prepareDf4SubjectWithBehaviorCodes('child')
cluster_kmeans('mother')

# convertToFrequencyRatioBySubjectCategory('mother')
