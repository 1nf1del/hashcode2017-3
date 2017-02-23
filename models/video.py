from math import inf


class Video:

    def __init__(self, id, size=inf):
        self.id = id
        self.size = size
        self.caches = {}

    def isInCache(self, cacheID):
        return cacheID in self.caches

    def addToCache(self, cache):
        self.caches[cache.getID()] = cache

    def setSize(self, size):
        self.size = size

    def getSize(self):
        return self.size

    def getID(self):
        return self.id

    def __repr__(self):
        return str(self.id)

    def __str__(self):
        return self.__repr__()
