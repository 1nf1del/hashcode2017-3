from collections import defaultdict
from math import inf


class Cache:

    def __init__(self, id, totalCapacity):
        self.id = id
        self.videos = {}
        self.latencyTo = defaultdict(int)
        self.endpoints = []
        self.usedCapacity = 0
        self.totalCapacity = totalCapacity

    def addEndpoint(self, endpoint, latency):
        self.latencyTo[endpoint] = latency
        self.endpoints.append(endpoint)

    def hasVideo(self, videoID):
        return videoID in self.videos

    def empty(self):
        return len(self.videos) == 0

    def addVideo(self, video):
        self.videos[video.getID()] = video
        self.usedCapacity += video.getSize()

    def fitsVideo(self, video):
        return self.usedCapacity + video.getSize() <= self.totalCapacity

    def getID(self):
        return self.id

    def getLatency(self, endpoint):
        if endpoint in self.latencyTo:
            return self.latencyTo[endpoint]
        return inf

    def __repr__(self):
        return "%s " % str(self.id) + ' '.join(map(str, self.videos.keys()))
