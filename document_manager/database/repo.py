from document_manager.database.field import Field
from document_manager.database.field import Tag
from document_manager.database.document_set import DocumentSet
from document_manager.database.document import Document
from document_manager.settings import debug

import os

class Repo:
	def __init__(self, repoDirPath):
		# Add trailing slash if missing
		if repoDirPath[-1] != "/" and repoDirPath[-1] != "\\":
			repoDirPath += "/"

		self.repoDirPath = repoDirPath

		self.name = "NOT_SET"
		self.layerNames = []
		self.headers = []

		self.counter = -1
		self.fields = []
		self.documentSets = []

		# Ensure repo exists in proper configuration
		if not os.path.exists(repoDirPath + "repo-config") or \
		   not os.path.exists(repoDirPath + "repo-data") or \
		   not os.path.exists(repoDirPath + "repo-documents/"):
			debug("ERROR: Repo not properly configured. repoDirPath=" + repoDirPath)
			return

		# Read Repo Configuration
		if not self.readConfig():
			debug("ERROR: Repo configuration invalid.")
			return

		# Read Repo Data
		if not self.readData():
			debug("ERROR: Repo data invalid.")
			return


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


	def readConfig(self):
		with open(self.repoDirPath + "repo-config", "r") as f:
			mode = "NONE"
			for line in f:
				line = line.strip('\n')
				# Check for mode change
				if line == "#Name":
					mode = "name"
				elif line == "#LayerNames":
					mode = "layerNames"
				elif line == "#Headers":
					mode = "headers"
				# Read payload data
				else:
					if mode == "name":
						self.name = line
					elif mode == "layerNames":
						self.layerNames.append(line)
					elif mode == "headers":
						# TODO configure custom header support
						self.headers.append(line)
					else:
						debug("Unused data in repo-config: " + self.repoDirPath + "repo-config")
		
		# Check for invalid data
		if self.name == "NOT_SET":
			return False
		
		return True


	def readData(self):
		with open(self.repoDirPath + "repo-data", "r") as f:
			mode = "NONE"
			for line in f:
				line = line.strip('\n')
				# Check for mode change
				if line == "#Counter":
					mode = "counter"
				elif line == "#Fields":
					mode = "fields"
				elif line == "#DocumentSets":
					mode = "documentSets"
				# Read payload data
				else:
					if mode == "counter":
						self.counter = int(line)
					elif mode == "fields":
						self.fields.append(self.parseField(line))
					elif mode == "documentSets":
						self.documentSets.append(self.parseDocEntry(line))
					else:
						debug("Unused data in repo-data: " + repoDirPath + "repo-data")

		# Check for invalid data
		if self.counter == -1:
			return False
		
		return True

	
	def parseField(self, line):
		line = line.split(',')

		# Parse resourceID, name, and type
		resourceID = line[0]
		name = line[1]
		type = line[2]

		# Parse tags
		tags = []
		if len(line) > 3:
			for pair in line[3:]:
				pair = pair.split(':')
				tags.append(Tag(pair[0], pair[1]))

		return Field(resourceID, name, type, tags)

	def parseDocEntry(self, entry):
		# Parse a set
		if entry[0] == '{':
			# Get ResourceID
			cursor = entry.find(',')
			setRID = entry[1:cursor]

			# Get elements
			setDocElements = []
			while cursor < len(entry)-2:
				# Get the element string
				cursor += 1
				startPos = cursor
				stack = [entry[cursor]]
				cursor += 1
				while len(stack) > 0:
					cursor += 1
					if entry[cursor] == '{' or entry[cursor] == '[':
						stack.append(entry[cursor])
					elif entry[cursor] == '}' and stack[-1] == '{':
						del stack[-1]
					elif entry[cursor] == ']' and stack[-1] == '[':
						del stack[-1]

				# Add the element
				setDocElements.append(self.parseDocEntry(entry[startPos:cursor+1]))

			return DocumentSet(setRID, setDocElements)

		# Parse a document		
		elif entry[0] == '[':
			entry = entry[1:-1].split(',')
			docRID = entry[0]
			extension = entry[1]
			descriptors = []
			for descriptor in entry[2:]:
				descriptors.append([descriptor.split(':')[0], descriptor.split(':')[1]])
			return Document(docRID, extension, descriptors)