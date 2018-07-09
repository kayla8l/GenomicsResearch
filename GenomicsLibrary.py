import csv
import numpy as np
from collections import defaultdict
from collections import Counter
from numpy import random
from datetime import datetime

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
        self.state = data[5]
        self.group = data[7]

    def print(self):
        print("chrX: " + self.chrX)
        print("start:", self.start)
        print("end: ", self.end)
        print("state: " + self.state)
        print("group: " + self.group)

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