
#Uber final Project! UBER Problem 
import csv
import pprint
import matplotlib.pyplot as plt
pp = pprint.PrettyPrinter()


class driver(object):
    def __init__(self):
        self.startTime = 0
        self.endTime = 0
        self.position = 0

    def __str__(self):
        return "position:"+ str(self.position)+ " endTime:"+ str(self.endTime)


    def getTimeToArrive(self,time, newPos, network_):
        timediff = 0
        if self.endTime>time:
            timediff = self.endTime - time
        newtime = timediff+ network_[self.position][newPos]
        return newtime
   
class request(object):
    def __init__(self,time_,start_,end_):
        self.time = time_
        self.start = start_
        self.end = end_

    def __str__(self):
        return "time:" + str(self.time) + " start:"+ str(self.start)+  " end:"+ str(self.end) 


def extractData(file1,file2):
    #Read CSV files into project 
    network = []
    with open(file1) as csvfile:
        reader = csv.reader(csvfile, delimiter = ",")
        for row in reader:
            newRow = []
            for elem in row:
                newRow.append(int(elem))
            network.append(newRow)

    #replace with real program
    requests = []
    with open(file2) as csvfile:
        reader = csv.reader(csvfile,delimiter = ",")
        for row in reader:
            requests.append(request(int(row[0]),int(row[1])-1,int(row[2])-1))
    return (network,requests)
#pp.pprint(requests)


def getMinDistMatrix(adjmatrix):
    #Floyd Warshal Algorithm for finding all minumum paths
    dist = []
    for i,row in enumerate(adjmatrix):
        distRow = []
        for j,elem in enumerate(row):
            if(elem == 0):
                elem = float("inf")
            if(i == j):
                elem = 0
            distRow.append(elem)
        dist.append(distRow)
    
    for k in range(len(adjmatrix)):
        for i in range(len(adjmatrix)):
            for j in range(len(adjmatrix)):
                if dist[i][j]>dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist

def getSortedNodes(network):
    weights = []
    for row in network:
        weights.append(sum(row))
    nodes = [x for x in range(len(network))]

    sortedNodes = sorted(nodes,key = lambda x:weights[x])
    print(sortedNodes)
    return sortedNodes

def getMinDriver(time,request_,drivers,network_,sortedNodes):
    minDrivers = []
    minTime = float("inf")
    for d in drivers:
        curTime = d.getTimeToArrive(time, request_.start,network_)
        print("curTime: "+ str(curTime))
        if curTime < minTime:
            minTime = curTime
            minDrivers = [d]
        elif curTime == minTime:
            minDrivers.append(d)
    bestDriver = max(minDrivers, key =lambda x:sortedNodes.index(x.position))
    print("Drivers")
    
    for d in drivers:
        print(d)
        print(d.getTimeToArrive(time, request_.start,network_))
    
    print("bestDriver")
    print(bestDriver)
    print(bestDriver.getTimeToArrive(time, request_.start,network_))
    return bestDriver



def AllocateDrivers(numOfDrivers,requests,minNetwork_,sortedNodes):
    #set up drivers
    drivers = [ driver() for i in range(numOfDrivers)]
    for i,dr in enumerate(drivers):
        dr.position = sortedNodes[i%len(sortedNodes)]
    #initialize wait time
    waitTime = 0
    
    #loop through request
    for req in requests:
        print("**************************")
        time = req.time
        #endTimes
        for d in drivers:
            if (d.endTime < time):
                d.endTime = time
        #print state of drivers  and request
        print("request-> "+ str(req))

        #pick the new driver

        bDriver = getMinDriver(time,req,drivers,minNetwork_,sortedNodes)
        #d = min(drivers,key = lambda d:d.getTimeToArrive(time,req.start,minNetwork))
        #add wait time
        print("Picked Drivers ---------")  
        print(bDriver)
        print(bDriver.getTimeToArrive(time,req.start,minNetwork_))
        print(waitTime)
        waitTime += bDriver.getTimeToArrive(time,req.start,minNetwork_)
        print(waitTime)
        print("Time waited for = " + str(bDriver.getTimeToArrive(time,req.start,minNetwork_)))
        #set new start and end possitions of driver
        
        bDriver.endTime  = bDriver.endTime + minNetwork_[bDriver.position][req.start] + minNetwork_[req.start][req.end]
        bDriver.position = req.end
       
       
        print("Driver Picked "+ str(drivers.index(bDriver)))
        print(bDriver)
    
    print("Total wait time:"+ str(waitTime))
    return waitTime

def GenerateHistogram(network_,requests_):
    pos = [x for x in range(len(network_))]
    fequencys = [0 for x in range(len(network_))]
    for req in requests_:
        fequencys[req.start] +=1
    plt.bar(pos,fequencys)
    plt.show()



#main runtime
if __name__ == "__main__":
    network,requests = extractData("network.csv","supplementpickups.csv")
    minNetwork = getMinDistMatrix(network)
    connectedness = getSortedNodes(minNetwork)
    #AllocateDrivers(400,requests,minNetwork,getSortedNodes(minNetwork))
    
    waitTimes = []
    driverNums = [10*x for x in range(1,10)]
    for i in driverNums:
        waitTimes.append(AllocateDrivers(i,requests,minNetwork,connectedness))

    #plt.plot(driverNums,waitTimes)
    #plt.show()
    GenerateHistogram(minNetwork,requests)








