import csv

##### Handle Locations #####

class Location(object):
    chrX = ""
    pos = 0
    states = []
    
    def __init__(self, chrX, pos, states):
        self.chrX = chrX
        self.pos = pos
        self.states = states

    def print(self):
        print("chrX: " + self.chrX)
        print("pos: ", self.pos)
        print("states: ", self.states)

def retrieveLocations(filename):
    locations = []
    filetype = filename.split(".")[-1]
    with open(filename) as file:
        if filetype == "txt":
            for i,line in enumerate(file):  
                if i == 0:
                    continue # ignore the header  
                location_data = line.split('\t')
                locationObj = Location(location_data[1], int(location_data[2]), [])
                locations.append(locationObj)
        else:
            data = list(csv.reader(file, delimiter=','))
            headers = data.pop(0) # remove the header from the data
            for row in data:
                locationObj = Location(row[1], int(row[2]), [])
                locations.append(locationObj)
    return locations
