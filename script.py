import Locations as lLib
import Logic as logic 
from collections import defaultdict
from datetime import datetime

startTime = datetime.now()

ranges, rangesByChrX, chromosomes, states = logic.parseRanges('BrainRanges.csv')

print("Chromosomes: ", chromosomes)
for chrX, chrList in rangesByChrX.items():
     print(chrX + " has ", len(chrList))
print("States: ", states)

### Retrieve the location data from files ###

sigLocations = lLib.retrieveLocations("list_Significant_cpg_locations_6895sites.txt") # holds the significant locations
refLocations = lLib.retrieveLocations("list_450K_cpg_locations.txt") # holds the reference locations

print("Number of significant locations: ", len(sigLocations))
sigLocations[0].print()

print("Number of reference locations: ", len(refLocations))
refLocations[0].print()

##### Data structures for results #####

sigResults = dict.fromkeys(states, 0) # dictionary with {state: # of overlaps ...}
refResults = dict.fromkeys(states, 0) # dictionary with {state: # of overlaps ...}

##### CREATE THE MAPPINGS #####

# print("Creating mapping for significant locations")
# logic.createMapping(sigLocations, "sigLocationsMapTest", rangesByChrX, states)

# print("Creating mapping for reference locations")
# createMapping(refLocations, "refLocationsMapTest", rangesByChrX, states)

### RUNNING THE TRIALS ###

refMappings = logic.readMapping('refLocationsMap.csv')
sigMappings = logic.readMapping('sigLocationsMap.csv')

trials = 100
logic.getResults(sigMappings, sigResults)
print("Results from significant locations")
print(sigResults)
trialResults, overallResults = logic.runTrials(trials, refMappings, sigLocations, sigResults, states) # list of results from trials

print("Number of results from trials ", len(trialResults))
print("Overall results from trials")
print(overallResults)

print("Overall odd-ratios")
refResultsAvgs = logic.calculateOddRatio(trialResults, sigResults, states)
print(refResultsAvgs)

pResults = logic.calculatePValue(overallResults, states, trials)
print("Overall p-values")
print(pResults)

print("Time elapsed: ", datetime.now() - startTime)



