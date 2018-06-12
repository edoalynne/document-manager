class Tag:
    def __init__(self, resourceID, value):
        self.resourceID = resourceID
        self.value = value

    def __str__(self):
        return self.resourceID + ":" + self.value