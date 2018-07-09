import Ranges
import Locations

##### Check for overlaps using the significant locations and appends state to the location #####

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

# Add results from dictionary with {state: # of overlaps ...} to {state: [overlaps from trial 1, ...]}

def mergeResults(results, sigResults, mainResults):
    for state, overlaps in results.items():
        sigOverlaps = sigResults[state]
        #print("Found  " , overlaps, " in " + state + " compared to ", sigOverlaps, " significant")
        if sigOverlaps == overlaps:
            mainResults[state] += 1

# Checks the overlap according to the ranges and saves the mapping of locations to states

def createMapping(locations, mapName, rangeDict, states):
    results = dict.fromkeys(states, 0) # dictionary with {state: # of overlaps ...}
    checkOverlaps(locations, rangeDict)
    with open(mapName + '.csv','w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for location in locations:
            states_dict = '/'.join(location.states) 
            writer.writerow([location.chrX, location.pos, states_dict])

# Reads in the mapping from a csvfile and returns the data as a list of locations

def readMapping(mapFile):
    with open(mapFile) as csvfile:
        mapData = list(csv.reader(csvfile, delimiter=','))
        mappedLocations = []
        for row in mapData:
            location = Location(row[0], int(row[1]), row[2].split('/'))
            mappedLocations.append(location)
    return mappedLocations