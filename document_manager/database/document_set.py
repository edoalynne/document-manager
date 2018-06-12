from document_manager.database.document_element import DocumentElement

class DocumentSet(DocumentElement):
    def __init__(self, resourceID, elements):
        self.resourceID = resourceID
        self.elements = elements

    def __str__(self):
        s = "{" + self.resourceID + ","
        for element in self.elements:
            s += str(element)  
        s += "}"
        return s