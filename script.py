import csv
import Ranges
import Locations
import Logic
import numpy as np
from collections import defaultdict
from collections import Counter
from numpy import random
from datetime import datetime

startTime = datetime.now()

ranges = extractRangesFromCSV('BrainRanges.csv') # holds the range objects
print("Number of ranges: ", len(ranges))
#ranges[0].print()

rangesByChrX = makeRangesDict(ranges)

print("Test")
print(rangesByChrX['X'][0].end)
print(rangesByChrX['X'][5].end)

chromosomes = getChromosomes(rangesByChrX)
print("Chromosomes: ", chromosomes)
#for chrX, chrList in rangesByChrX.items():
#     print(chrX + " has ", len(chrList))

states = getStates(ranges)
print("States: ", states)

### Retrieve the location data from files ###

sigLocations = retrieveLocations("list_Significant_cpg_locations_6895sites.txt") # holds the significant locations
refLocations = retrieveLocations("list_450K_cpg_locations.txt") # holds the reference locations

# print("Number of significant locations: ", len(sigLocations))
# sigLocations[0].print()

# print("Number of reference locations: ", len(refLocations))
# refLocations[0].print()

##### Data structures for results #####

sigResults = dict.fromkeys(states, 0) # dictionary with {state: # of overlaps ...}
refResults = dict.fromkeys(states, 0) # dictionary with {state: # of overlaps ...}

##### Pick randomly from the other reference #####

# add results from dictionary with {state: # of overlaps ...} to {state: [overlaps from trial 1, ...]}
def mergeResults(results, sigResults, mainResults):
    for state, overlaps in results.items():
        sigOverlaps = sigResults[state]
        #print("Found  " , overlaps, " in " + state + " compared to ", sigOverlaps, " significant")
        if sigOverlaps == overlaps:
            mainResults[state] += 1

# checks the overlap according to the ranges and saves the mapping of locations to states
def createMapping(locations, mapName, rangeDict, states):
    results = dict.fromkeys(states, 0) # dictionary with {state: # of overlaps ...}
    checkOverlaps(locations, rangeDict)
    with open(mapName + '.csv','w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for location in locations:
            states_dict = '/'.join(location.states) #Counter(location.states) 
            writer.writerow([location.chrX, location.pos, states_dict])

# print("Creating mapping for significant locations")
# createMapping(sigLocations, "sigLocationsMap", rangesByChrX, states)
# getResults(sigLocations, sigResults)
# print("Results from significant locations")
# print(sigResults)

# print("Creating mapping for reference locations")
# createMapping(refLocations, "refLocationsMap", rangesByChrX, states)
# getResults(refLocations, refResults)
# print("Results from reference locations")
# print(refResults)

# reads in the mapping from a csvfile and returns the data as a list of locations
def readMapping(mapFile):
    with open(mapFile) as csvfile:
        mapData = list(csv.reader(csvfile, delimiter=','))
        mappedLocations = []
        for row in mapData:
            location = Location(row[0], int(row[1]), row[2].split('/'))
            mappedLocations.append(location)
    return mappedLocations

refMappings = readMapping('refLocationsMap.csv')
sigMappings = readMapping('sigLocationsMap.csv')

trials = 10000
getResults(sigMappings, sigResults)
print("Results from significant locations")
print(sigResults)
refResults = dict.fromkeys(states, 0) # dictionary with {state: # of times it has same overlap as significant}
refResultsRaw = []

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

print("Number of results from trials ", len(refResultsRaw))

print("Overall results from trials")
print(refResults)

### Calculating the odd ratio ###

refResultsAvgs = dict.fromkeys(states, 0.0) # dictionary with {state: # avg of times this state appeared}
for state, avg in refResultsAvgs.items():
 state_results = []
 for result in refResultsRaw:
  state_results.append(result[state])
 avg = np.mean(state_results)
 print("Avg: ", avg)
 refResultsAvgs[state] = sigResults[state] / avg

print("Overall odd-ratios")
print(refResultsAvgs)

### Calculating the p-value ###

pResults = dict.fromkeys(states, 0) # dictionary with {state: p-value}

for state, overlaps in refResults.items():
    same_overlap_as_significant = overlaps
    pResults[state] = float(same_overlap_as_significant / trials)

print("Overall p-values")
print(pResults)

print("Time elapsed: ", datetime.now() - startTime)



