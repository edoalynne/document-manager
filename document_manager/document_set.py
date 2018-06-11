from document_manager.doc_element import DocElement

class DocumentSet(DocElement):
    def __init__(self, resourceID, docElements):
        self.resourceID = resourceID
        self.docElements = docElements

    def __str__(self):
        s = "resourceID=" + self.resourceID + "\n"
        for d in self.docElements:
            s += str(d) + "\n"
        s += "--"
        return s