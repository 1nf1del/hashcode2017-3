from collections import defaultdict
from math import inf


class Endpoint:

    def __init__(self, id, latencyToDatacenter=inf):
        self.id = id
        self.requests = []
        self.latencyTo = defaultdict(int)
        self.latencyToDatacenter = latencyToDatacenter
        self.caches = []

    def addRequest(self, r):
        self.requests.append(r)

    def getNumberOfRequests(self):
        return len(self.requests)

    def getID(self):
        return self.id

    def sortRequestsByQuantity(self):
        self.requests = sorted(self.requests,
                               key=lambda r: r.getQuantity(),
                               reverse=True)

    def getNextRequest(self):
        for r in self.requests:
            yield r

    def addCache(self, cache, latency):
        self.latencyTo[cache] = latency
        self.caches.append(cache)

    def getLatencyImprovement(self, cache):
        if cache in self.latencyTo:
            return self.latencyToDatacenter - self.latencyTo[cache]
        return inf

    def setLatencyToDatacenter(self, latency):
        self.latencyToDatacenter = latency

    def getLatencyToDatacenter(self, latency):
        return self.latencyToDatacenter

    def getNthRequest(self, n):
        return self.requests[n]

    def hasAccessToVideo(self, video):
        for cache in self.caches:
            if cache.hasVideo(video.getID()):
                return True
        return False
