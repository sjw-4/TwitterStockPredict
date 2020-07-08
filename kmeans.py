import random as rnd
from scipy.spatial import distance as ds
import numpy as np
import utils
import copy

class KMeans:
    def __init__(self, _data, _n_clusters=3, _maxIters=100, _name=None):
        if _name != None:
            self.filePath = "Data/kmeans_" + str(_name) + ".json"
            self.centroids = utils.loadData(self.filePath)
        else:
            self.centroids = []         #centroids
            self.filePath = None        #filepath to save/load data

        self.data = _data               #Two dimensional array [[]]
        self.n_clusters = _n_clusters   #number of clusters to use
        self.maxIters = _maxIters       #max number of iterations when training

    def __improveCentroids(self):
        closestCent = copy.deepcopy(self.centroids)
        for i in range(len(closestCent)): closestCent[i].append(1000)
        for dat in self.data:
            d = dat.tolist()
            for i in range(len(closestCent)):
                tempDist = ds.euclidean(d, self.centroids[i])
                if tempDist < closestCent[i][-1]: closestCent[i] = d + [tempDist]
        self.centroids = []
        for c in closestCent:
            self.centroids.append(c[:-1])

    def train(self, _startPos=None):
        #randomly generate centroid location between -1 and 1
        if _startPos == None:
            self.centroids = []
            for i in range(self.n_clusters):
                cent = []
                for i in range(len(self.data[0])):
                    cent.append(rnd.uniform(-1, 1))
                self.centroids.append(cent)
        else:
            self.centroids = _startPos
        self.__improveCentroids()
        
        #begin calculating the centers
        for i in range(self.maxIters):
            #assign data to centroids
            centroidData = [[]] * self.n_clusters
            for j in range(len(centroidData)): centroidData[j] = []
            for item in self.data:
                distance = []
                for cent in self.centroids:
                    distance.append(ds.euclidean(item, cent))
                centroidData[distance.index(min(distance))].append(item.tolist())
            #recalculate centroids
            self.centroids = [[0] * len(self.centroids[0])] * len(self.centroids)
            for j in range(len(centroidData)):
                for cent in centroidData[j]:
                    self.centroids[j] = [a + b for a, b in zip(self.centroids[j], cent)]
                self.centroids[j] = [x / len(centroidData[j]) for x in self.centroids[j]]
            '''newCent = [0] * len(centroidData[j])
                for k in range(len(centroidData[j])):
                    newCent[k] = [0] * len(centroidData[j][k])
                    newCent[k] = np.add(newCent[k], centroidData[j][k])     #.tolist()
                self.centroids[j] = [x / len(centroidData[j]) for x in newCent[j]]'''

        #save data
        if self.filePath != None:
            utils.saveData(self.filePath, self.centroids)

    def predict(self, _data):
        if len(_data) != len(self.centroids[0]):
            print("Error:kmeans:predict: unequal lengths - " + str(len(_data)) + ", " + str(len(self.centroids[0])))
        
        distance = []
        for cent in self.centroids:
            distance.append(ds.euclidean(_data, cent))
        return distance.index(min(distance))

    def printCentroids(self):
        if self.centroids == []:
            return "Centroids not yet calculated"
        else:
            output = ""
            for i in range(len(self.centroids)):
                output += str(i) + ": "
                for cent in self.centroids[i]:
                    output += str(cent) + ", "
                output = output[:-2] + "\n"
            return output[:-1]