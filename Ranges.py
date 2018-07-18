import csv
from collections import defaultdict

##### Handle ranges ######

class Range(object):
    chrX = ""
    start = 0
    end = 0
    state = ""
    group = ""

    def __init__(self, data):
        self.chrX = data[0].split("chr")[1]
        self.start = int(data[1])
        self.end = int(data[2])
        self.state = data[3]

    def print(self):
        print("chrX: " + self.chrX)
        print("start:", self.start)
        print("end: ", self.end)
        print("state: " + self.state)

### Extract the ranges from a csv file ###

def extractRangesFromCSV(filename):
    ranges = []
    with open(filename) as csvfile:
        rangeData = list(csv.reader(csvfile, delimiter=','))
        headers = rangeData.pop(0) # remove the header from the data
        for row in rangeData:
            rangeObj = Range(row)
            ranges.append(rangeObj)
    return ranges

### Extract the ranges from a BED file ###

def extractRangesFromBED(filename):
    ranges = []
    with open(filename) as file:
        rangeData = list(csv.reader(file, delimiter='\t'))
        for row in rangeData:
            rangeObj = Range(row)
            ranges.append(rangeObj)
    return ranges

### Returns a dict of ranges organized by chromosome and sorted by start position ###

def makeRangesDict(ranges):
    rangesByChrX = defaultdict(list) 
    for rangeObj in ranges:
        rangesByChrX[rangeObj.chrX].append(rangeObj)

    ### Sort the ranges by the start position, to make things go faster ###
    for chrom, chromRanges in rangesByChrX.items():
        chromRanges.sort(key=lambda chromRange: chromRange.end, reverse=True)
    return rangesByChrX

### Returns the unique list of chromosomes ###

def getChromosomes(rangeDict):
    return list(rangeDict.keys())

### Returns the unique list of states ###

def getStates(ranges):
    rangesByStates = defaultdict(list)
    for rangeObj in ranges:
        rangesByStates[rangeObj.state].append(rangeObj)
    return list(rangesByStates.keys())
