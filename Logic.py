import csv
import Ranges as rLib
from Locations import Location
from numpy import random
import numpy as np

### Parse the ranges from a given file (csv or bed) and return data ###

def parseRanges(filename):
    print("Parsing ranges from " + filename + "...")
    filetype = filename.split(".")[-1]
    ranges = [] # holds the range objects
    if filetype == 'csv':
        print("Extracting from CSV file")
        ranges = rLib.extractRangesFromCSV(filename) 
    else:
        print("Extracting from BED file")
        ranges = rLib.extractRangesFromBED(filename)
    print("Number of ranges: ", len(ranges))
    rangesByChrX = rLib.makeRangesDict(ranges)
    chromosomes = rLib.getChromosomes(rangesByChrX)
    states = rLib.getStates(ranges)
    return ranges, rangesByChrX, chromosomes, states

### Check for overlaps using the significant locations and appends state to the location ###

def checkOverlaps(locations, rangeDict):
    for location in locations:
        chrom = location.chrX
        chromRanges = rangeDict[chrom] # gets the list of relevant ranges
        location_states = []
        for chromRange in chromRanges:
            if chromRange.start <= location.pos <= chromRange.end:
                location_states.append(chromRange.state)
        location.states = location_states

### Get results after checking locations for overlap with ranges ###

def getResults(locations, results):
    for location in locations:
        for state in location.states:
            if state != '':
                results[state] += 1

### Add results from dictionary with {state: # of overlaps ...} to {state: [overlaps from trial 1, ...]} ###

def mergeResults(results, sigResults, mainResults):
    for state, overlaps in results.items():
        sigOverlaps = sigResults[state]
        #print("Found  " , overlaps, " in " + state + " compared to ", sigOverlaps, " significant")
        if overlaps >= sigOverlaps:
            mainResults[state] += 1

### Checks the overlap according to the ranges and saves the mapping of locations to states ###

def createMapping(locations, mapName, rangeDict, states):
    results = dict.fromkeys(states, 0) # dictionary with {state: # of overlaps ...}
    checkOverlaps(locations, rangeDict)
    with open(mapName + '.csv','w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for location in locations:
            states_dict = ';'.join(location.states) 
            writer.writerow([location.chrX, location.pos, states_dict])
    results = dict.fromkeys(states, 0) # dictionary with {state: # of overlaps ...}
    getResults(locations, results)
    print("Results from locations")
    print(results)

### Reads in the mapping from a csvfile and returns the data as a list of locations ###

def readMapping(mapFile):
    with open(mapFile) as csvfile:
        mapData = list(csv.reader(csvfile, delimiter=','))
        mappedLocations = []
        for row in mapData:
            location = Location(row[0], int(row[1]), row[2].split(';'))
            mappedLocations.append(location)
    return mappedLocations

### Runs the trials and returns a list of the results ###

def runTrials(trials, refMappings, sigLocations, sigResults, states):
    refResultsRaw = []
    refResults = dict.fromkeys(states, 0) # dictionary with {state: # of times it has same overlap as significant}
    for i in range(0, trials):
     chosenLocations = random.choice(refMappings, len(sigLocations)) # randomly pick the same # of significant sites from the reference
     results = dict.fromkeys(states, 0) # dictionary with {state: # of overlaps ...}
     for location in chosenLocations:
        for state in location.states:
            if state != '':
                results[state] += 1
     print("Results from trial ", i + 1)
     print(results)
     mergeResults(results, sigResults, refResults)
     refResultsRaw.append(results)
    return refResultsRaw, refResults

### Calculating the odd ratio and returning results as a dict ###

def calculateOddRatio(trialResults, sigResults, states):
    refResultsAvgs = dict.fromkeys(states, 0.0) # dictionary with {state: # avg of times this state appeared}
    for state, avg in refResultsAvgs.items():
     state_results = []
     for result in trialResults:
      state_results.append(result[state])
     avg = np.mean(state_results)
     print("Avg: ", avg)
     refResultsAvgs[state] = sigResults[state] / avg
    return refResultsAvgs

### Calculating the p-value and returning results as a dict ###

def calculatePValue(refResults, states, trials):
    pResults = dict.fromkeys(states, 0) # dictionary with {state: p-value}
    for state, overlaps in refResults.items():
        same_overlap_as_significant = overlaps
        pResults[state] = float((same_overlap_as_significant + 1)/ (trials + 1))
    return pResults
