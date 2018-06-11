from document_manager.doc_element import DocElement

class Document(DocElement):
    def __init__(self, resourceID, extension, descriptors):
        self.resourceID = resourceID
        self.extension = extension
        self.descriptors = descriptors

    def __str__(self):
        return "RID=" + self.resourceID + ", extension=" + self.extension + ", descriptors=" + str(self.descriptors)
