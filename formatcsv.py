import sys
import csv
import filecmp
import os.path
from pathlib import Path
from collections import OrderedDict
from shutil import copy2

headerLength = 0
baseColumns = 4

# CSV filenames
confirmedFileName: str = 'time_series_covid19_confirmed_global.csv'
deathsFileName: str = 'time_series_covid19_deaths_global.csv'
# recoveredFileName: str = 'time_series_19-covid-Recovered.csv'
originalFilesList = [confirmedFileName, deathsFileName]
suffix = '_old'


def mutate_csv(file_path):
    with open(file_path) as file:
        fileLines = file.read().splitlines()
        originalCSVDict = csv.DictReader(fileLines)
        rows = [row for row in originalCSVDict]
        numberOfDates = len(originalCSVDict.fieldnames)

        newCsv = []
        for i in range(4, numberOfDates):
            for row in rows:
                items = list(row.items())
                myDict = OrderedDict([(items[0][0], items[0][1])])
                for dictIter in range(1, 4):
                    myDict[items[dictIter][0]] = items[dictIter][1]
                myDict['Date'] = items[i][0]
                myDict['Cases'] = items[i][1]
                newCsv.append(myDict)
        return newCsv


def check_files_changed(file_path, new_files, previous_files):
    filesChanged = False
    previousFileList = [Path(file_path + '/' + previous_files[0]), Path(file_path + '/' + previous_files[1])]

    for file in previousFileList:
        if not file.is_file():
            with open(file, 'w+') as newFile:
                newFile.close()

    for index in range(0, 2):
        if not os.path.isfile(file_path + '/' + 'formatted-' + new_files[index]):
            print('File "%s" does not exist' % ('formatted-' + new_files[index]))
            filesChanged = True
        if not filecmp.cmp(Path(file_path + '/' + new_files[index]), previousFileList[index]):
            print('File "%s" differs' % previousFileList[index])
            filesChanged = True

        else:
            print('File "%s" did not change' % previousFileList[index])
    return filesChanged


if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = '~/'
filesHaveChanged = check_files_changed(path, [confirmedFileName, deathsFileName],
                                       [confirmedFileName + suffix, deathsFileName + suffix])
if filesHaveChanged:
    for it in range(0, 2):
        with open(path + '/formatted-' + originalFilesList[it], 'w+', newline='') as newCSVFile:
            print('Editing formatted-' + originalFilesList[it])
            writer = csv.DictWriter(newCSVFile, ['Province/State', 'Country/Region', 'Lat', 'Long', 'Date', 'Cases'])
            newFiles = []
            writer.writeheader()
            newFiles.append(mutate_csv(path + '/' + originalFilesList[it]))
            copy2(path + '/' + originalFilesList[it], path + '/' + originalFilesList[it] + suffix)
            writer.writerows(newFiles[it-1])
