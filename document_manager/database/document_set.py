from document_manager.database.document_element import DocumentElement

class DocumentSet(DocumentElement):
    def __init__(self, resourceID, elements):
        self.resourceID = resourceID
        self.elements = elements

    def __str__(self):
        s = "resourceID=" + self.resourceID + "\n"
        for d in self.elements:
            s += str(d) + "\n"
        s += "--"
        return s