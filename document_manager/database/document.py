from document_manager.database.document_element import DocumentElement

class Document(DocumentElement):
    def __init__(self, resourceID, extension, descriptors):
        self.resourceID = resourceID
        self.extension = extension
        self.descriptors = descriptors

    def __str__(self):
        return "RID=" + self.resourceID + ", extension=" + self.extension + ", descriptors=" + str(self.descriptors)
