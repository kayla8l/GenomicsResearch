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
    with open(filename) as file:
        for i,line in enumerate(file):  
            if i == 0:
                continue # ignore the header  
            location_data = line.split('\t')
            locationObj = Location(location_data[1], int(location_data[2]), [])
            locations.append(locationObj)
    return locations

