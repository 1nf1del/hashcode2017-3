class Request:

    def __init__(self, video=None, endpoint=None, quantity=0):
        self.video = video
        self.endpoint = endpoint
        self.quantity = quantity

    def setVideo(self, video):
        self.video = video

    def setEndpoint(self, endpoint):
        self.endpoint = endpoint

    def setQuantity(self, quantity):
        self.quantity = quantity

    def getVideo(self):
        return self.video

    def getQuantity(self):
        return self.quantity
