from document_manager.base_doc import BaseDoc

class Document(BaseDoc):
    def __init__(self):
        self.extension = ""
        self.tagPairs = []
