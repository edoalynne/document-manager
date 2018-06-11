from document_manager.database.field import Field
from document_manager.database.field import Tag
from document_manager.database.document_set import DocumentSet
from document_manager.database.document import Document

class Repo:
	def __init__(self, name, layerNames, headers, counter, fields, documentSets):
		self.name = name
		self.layerNames = layerNames
		self.headers = headers

		self.counter = counter
		self.fields = fields
		self.documentSets = documentSets

	def __str__(self):
		s = "~~ Repo <" + self.repoDirPath + "> ~~\n"	
		s += "Repo Configuration:\n"
		s += "name=" + self.name + "\n"
		s += "layerNames=" + str(self.layerNames) + "\n"
		s += "headers=" + str(self.headers) + "\n"
		s += "Repo Data:\n"
		s += "counter=" + str(self.counter) + "\n"
		s += "fields=\n"
		for field in self.fields:
			s += "  ~  " + str(field) + "\n"
		s += "documentCount=" + str(len(self.documentSets))
		return s