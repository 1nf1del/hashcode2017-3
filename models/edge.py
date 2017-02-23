from models.endpoint import *
from models.cache import *


class Edge:

    def __init__(self, endpoint, cache):
        self.endpoint = endpoint
        self.cache = cache

    def getEndpoint(self):
        return self.endpoint

    def getCache(self):
        return self.cache

    def getCost(self):
        requests = self.endpoint.getNumberOfRequests()
        latencyImprovement = self.endpoint.getLatencyImprovement(self.cache)
        return requests * latencyImprovement

    def __gt__(self, other):
        return self.getCost() > other.getCost()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "(endpoint %i, cache %i, cost %i)" % \
            (self.endpoint.getID(), self.cache.getID(), self.getCost())
