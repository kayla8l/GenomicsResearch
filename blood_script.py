import Locations as lLib
import Logic as logic 
from collections import defaultdict
from datetime import datetime

experiment = "blood"

# For timing 
startTime = datetime.now()

# Load the range
range_name = "E039"
print("Using range " + range_name)
ranges, rangesByChrX, chromosomes, states = logic.parseRanges('E039_15_coreMarks_mnemonics.bed')

# Debug
print("Chromosomes: ", chromosomes)
for chrX, chrList in rangesByChrX.items():
	 print(chrX + " has ", len(chrList))
print("States: ", states)

# Retrieve location data
sigLocations = lLib.retrieveLocations("list_20k_blood_sig_locations.csv") # holds the significant locations
refLocations = lLib.retrieveLocations("list_436k_blood_locations.csv") # holds the reference locations

# Debug
print("Number of significant locations: ", len(sigLocations))
print("Number of reference locations: ", len(refLocations))

# Mappings
# print("Creating mapping for significant locations")
# logic.createMapping(sigLocations, "sigLocations_" + experiment + "_" + range_name, rangesByChrX, states)
# print("Creating mapping for reference locations")
# logic.createMapping(refLocations, "refLocations_" + experiment + "_" + range_name, rangesByChrX, states)

# Data structures for results 
sigResults = dict.fromkeys(states, 0) # dictionary with {state: # of overlaps ...}
refResults = dict.fromkeys(states, 0) # dictionary with {state: # of overlaps ...}

# Load mappings
refMappings = logic.readMapping("refLocations_" + experiment + "_" + range_name + '.csv')
sigMappings = logic.readMapping("sigLocations_" + experiment + "_" + range_name + '.csv')

# Run trials
trials = 10000
# logic.getResults(sigMappings, sigResults)
# print("Results from significant locations")
# print(sigResults)
# trialResults, overallResults = logic.runTrials(trials, refMappings, sigLocations, sigResults, states) # list of results from trials

# print("Number of results from trials ", len(trialResults))
# print("Overall results from trials")
# print(overallResults)

# print("Overall odd-ratios")
# refResultsAvgs = logic.calculateOddRatio(trialResults, sigResults, states)
# print(refResultsAvgs)

# pResults = logic.calculatePValue(overallResults, states, trials)
# print("Overall p-values")
# print(pResults)

# print("Time elapsed: ", datetime.now() - startTime)

# Re-calculate the p-values
E033_sig = {'15_Quies': 3080, '14_ReprPCWk': 2280, '10_TssBiv': 699, '13_ReprPC': 3455, '7_Enh': 2607, '9_Het': 22, '1_TssA': 1091, '2_TssAFlnk': 3058, '5_TxWk': 1729, '8_ZNF/Rpts': 14, '4_Tx': 535, '6_EnhG': 342, '12_EnhBiv': 375, '11_BivFlnk': 390, '3_TxFlnk': 182}
E033_overall = {'15_Quies': 0, '14_ReprPCWk': 10000, '10_TssBiv': 5394, '13_ReprPC': 10000, '7_Enh': 10000, '9_Het': 0, '1_TssA': 0, '2_TssAFlnk': 10000, '5_TxWk': 7, '8_ZNF/Rpts': 0, '4_Tx': 0, '6_EnhG': 10000, '12_EnhBiv': 10000, '11_BivFlnk': 4880, '3_TxFlnk': 10000}

E034_sig = {'15_Quies': 1319, '14_ReprPCWk': 2898, '13_ReprPC': 3594, '11_BivFlnk': 694, '12_EnhBiv': 2915, '9_Het': 24, '1_TssA': 417, '7_Enh': 2985, '2_TssAFlnk': 2516, '5_TxWk': 1121, '4_Tx': 399, '6_EnhG': 629, '3_TxFlnk': 275, '10_TssBiv': 45, '8_ZNF/Rpts': 23}
E034_overall = {'15_Quies': 0, '14_ReprPCWk': 0, '13_ReprPC': 10000, '11_BivFlnk': 0, '12_EnhBiv': 10000, '9_Het': 0, '1_TssA': 0, '7_Enh': 10000, '2_TssAFlnk': 10000, '5_TxWk': 0, '4_Tx': 0, '6_EnhG': 10000, '3_TxFlnk': 10000, '10_TssBiv': 0, '8_ZNF/Rpts': 6024}

E039_sig = {'15_Quies': 4867, '1_TssA': 750, '2_TssAFlnk': 3365, '14_ReprPCWk': 2362, '7_Enh': 3295, '9_Het': 28, '5_TxWk': 1648, '4_Tx': 388, '8_ZNF/Rpts': 43, '13_ReprPC': 1460, '12_EnhBiv': 727, '6_EnhG': 288, '3_TxFlnk': 308, '11_BivFlnk': 252, '10_TssBiv': 72}
E039_overall = {'15_Quies': 0, '1_TssA': 0, '2_TssAFlnk': 10000, '14_ReprPCWk': 10000, '7_Enh': 10000, '9_Het': 0, '5_TxWk': 8984, '4_Tx': 0, '8_ZNF/Rpts': 3235, '13_ReprPC': 10000, '12_EnhBiv': 10000, '6_EnhG': 10000, '3_TxFlnk': 0, '11_BivFlnk': 0, '10_TssBiv': 0}

# Need to reverse the overall because the >= was flipped earlier

for state, overlaps_less_than_sig in E039_overall.items():
	E039_overall[state] = trials - overlaps_less_than_sig

print(E039_overall)
print(logic.calculatePValue(E039_overall, states, trials))