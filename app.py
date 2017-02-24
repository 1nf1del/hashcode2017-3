from models.endpoint import *
from models.cache import *
from models.video import *
from models.request import *
from models.edge import *
from utils.logger import *
import traceback
import sys


class App:

    def __init__(self, inputFilename):
        self.logger = Logger(debug=True)

        self.numberOfEndpoints = 0
        self.numberOfCaches = 0
        self.numberOfVideos = 0

        self.endpoints = {}
        self.caches = {}
        self.videos = {}

        self.edges = []

        self.populateFromInputFile(inputFilename)

    def populateFromInputFile(self, inputFilename):
        try:
            with open(inputFilename, "r") as inputFile:
                self.numberOfVideos, \
                    self.numberOfEndpoints, \
                    self.numberOfRequests, \
                    self.numberOfCaches, \
                    self.cacheCapacity = App.readLineAsIntTuple(inputFile)

                self.createBlankEverything()
                self.readAndUpdateEverything(inputFile)

        except Exception as e:
            self.logger.log("Exception: %r" % e)
            traceback.print_exc()
            exit(1)

    def createBlankEndpoints(self):
        for i in range(self.numberOfEndpoints):
            self.endpoints[i] = Endpoint(i)

    def createBlankCaches(self):
        for i in range(self.numberOfCaches):
            self.caches[i] = Cache(i, self.cacheCapacity)

    def createBlankVideos(self):
        self.logger.log("Creating blank videos")
        for i in range(self.numberOfVideos):
            self.videos[i] = Video(i)
        self.logger.log("Done creating blank videos")

    def createBlankEverything(self):
        self.logger.log("Creating blank objects")

        self.createBlankEndpoints()
        self.createBlankCaches()
        self.createBlankVideos()

        self.logger.log("Done creating blank objects")

    def getNthEndpoint(self, n):
        return self.endpoints[n]

    def getNthCache(self, n):
        return self.caches[n]

    def getNthVideo(self, n):
        return self.videos[n]

    def readAndUpdateVideos(self, inputFile):
        self.logger.log("Reading and updating videos")

        videoSizes = App.readLineAsIntTuple(inputFile)

        for i, size in enumerate(videoSizes):
            self.getNthVideo(i).setSize(size)
        self.logger.log("Done reading and updating videos")

    def readAndUpdateEndpoints(self, inputFile):
        self.logger.log("Reading and updating endpoints")
        for i in range(self.numberOfEndpoints):
            latencyToDatacenter, numberOfCaches = App.readLineAsIntTuple(
                inputFile)

            currentEndpoint = self.getNthEndpoint(i)
            currentEndpoint.setLatencyToDatacenter(latencyToDatacenter)

            for j in range(numberOfCaches):
                cacheID, latency = App.readLineAsIntTuple(inputFile)

                cache = self.getNthCache(cacheID)

                currentEndpoint.addCache(cache, latency)
                cache.addEndpoint(currentEndpoint, latency)

                self.edges.append(Edge(currentEndpoint, cache))
        self.logger.log("Done reading and updating endpoints")

    def readAndUpdateRequests(self, inputFile):
        self.logger.log("Reading and updating requests")
        for i in range(self.numberOfRequests):
            videoID, endpointID, quantity = App.readLineAsIntTuple(inputFile)

            video = self.getNthVideo(videoID)
            endpoint = self.getNthEndpoint(endpointID)

            currentRequest = Request()
            currentRequest.setVideo(video)
            currentRequest.setEndpoint(endpoint)
            currentRequest.setQuantity(quantity)

            endpoint.addRequest(currentRequest)
        self.logger.log("Done reading and updating requests")

    def readAndUpdateEverything(self, inputFile):
        self.readAndUpdateVideos(inputFile)
        self.readAndUpdateEndpoints(inputFile)  # including caches
        self.readAndUpdateRequests(inputFile)

        for endpoint in self.endpoints.values():
            endpoint.sortRequestsByQuantity()

    def readLineAsIntTuple(inputFile):
        return map(int, inputFile.readline().split())

    def sortEdges(self):
        self.logger.log("Sorting edges")
        self.edges = sorted(self.edges, reverse=True)
        self.logger.log("Done sorting edges")

    def solveAllEdges(self):
        self.logger.log("Solving all edges")

        for i, edge in enumerate(self.edges):

            percentage = int(100 * i / len(self.edges))
            prevPercentage = int(100 * (i-1) / len(self.edges))

            if percentage != prevPercentage:
                self.logger.log("Completed %i%%" % percentage)

            self.solveOneEdge(edge)

        self.logger.log("Done solving all edges")

    def solveOneEdge(self, edge):
        endpoint = edge.getEndpoint()
        cache = edge.getCache()

        for request in endpoint.requests:
            self.solveOneRequest(endpoint, cache, request)

    def solveOneRequest(self, endpoint, cache, request):
        video = request.getVideo()

        if endpoint.hasAccessToVideo(video):
            return

        if cache.fitsVideo(video):
            cache.addVideo(video)
            video.addToCache(cache)

    def generateOutput(self):
        usedCaches = []
        usedCaches = [cache for cache in self.caches.values()
                      if not cache.empty()]

        ret = "%i\n" % len(usedCaches)
        for cache in usedCaches:
            ret += "%s\n" % str(cache)

        return ret.strip()
