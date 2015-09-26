# winner details
best_path = list()
best_drop = 0

def buildgraph(row, col, elevations):
    elevationdict = dict()
    graph = dict()
    id = 1
    for i in xrange(row):
        for j in xrange(col):
            elevationdict[id] = elevations[i][j]
            graph[id] = set()

            # check neighbours
            northid = id-col
            westid  = id-1

            if id == 1:
                # skip check for first node
                id += 1
                continue

            if id <= col:
                # if first row, check westid only
                if elevationdict[westid] > elevationdict[id]:
                    graph[westid].add(id)
                elif elevationdict[westid] < elevationdict[id]:
                    graph[id].add(westid)
            else:
                # second row onwards, check westid and northid
                if id%col != 1:
                    # if not first column, check westid
                    if elevationdict[westid] > elevationdict[id]:
                        graph[westid].add(id)
                    elif elevationdict[westid] < elevationdict[id]:
                        graph[id].add(westid)
                # everything else, check northid
                if elevationdict[northid] > elevationdict[id]:
                    graph[northid].add(id)
                elif elevationdict[northid] < elevationdict[id]:
                    graph[id].add(northid)

            id += 1

    return graph, elevationdict

def findlongestpath(graph, peaks):
    def findpaths(point,path=[]):
        if path == []:
            path = [point]
        else:
            path.append(point)
        # if end of path
        if len(graph[point]) == 0:
            global best_path
            global best_drop
            # if new path is longer than best path
            if len(path) > len(best_path):
                best_path = path[:]
                best_drop = drop(path)
            if len(path) == len(best_path):
                # if new drop is higher than best drop
                if drop(path) > best_drop:
                    best_path = path[:]
                    best_drop = drop(path) 
        # otherwise keep track of path
        for i in graph[point]:
            findpaths(i, path[:])

    for p in peaks:
        findpaths(p)

    return best_path, best_drop

def drop(path):
    return elevationdict[path[0]] - elevationdict[path[-1]]

import time
start_time = time.time()

print "Reading input file..."
#with open("map.txt") as f:
#    row, col = map(int, f.readline().split())
#    elevations = [map(int,l.split()) for l in f.readlines()]
row, col = map(int, raw_input().split())
elevations = []
for _ in xrange(row):
    elevations.append(map(int, raw_input().split()))

print "Building adjacency list..."
graph, elevationdict = buildgraph(row, col, elevations)

peaks = set(graph.keys()) - set().union(*graph.values())
print len(peaks), "peaks found"

print "Finding longest path..."
best_path, best_drop = findlongestpath(graph, peaks)

print "Found!"
print "Length: {0}, Drop: {1}".format(len(best_path), best_drop)
print "Elevation path:", [elevationdict[n] for n in best_path]

print "--- Completed in {0} seconds ---".format(time.time() - start_time)