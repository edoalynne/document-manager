from document_manager.tag import Tag

class Field:
    def __init__(self, resourceID, name, type, tags):
        self.resourceID = resourceID
        self.name = name
        self.type = type
        self.tags = tags

    def __str__(self):
        s = "resourceID=" + self.resourceID + "; "
        s += "name=" + self.name + "; "
        s += "type=" + self.type + "; "
        s += "tags=["
        for tag in self.tags:
            s += "(" + str(tag) + "),"
        if len(self.tags) > 0:
            s = s[:-1] + ']'
        else:
            s += "]"
        return s
