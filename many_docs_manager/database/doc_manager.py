import sqlite3

class DocManager:
	def __init__(self, database, cursor):
		self.db = database
		self.c = cursor

	def create(self, extension, parent_id, sort_order=0):
		# Verify extension
		if not self.__verifyExtension(extension):
			return False
	
		# Verify parent_id
		if not self.__verifyParentID(parent_id):
			return False

		# Verify sort_order
		parent_child_count = self.c.execute("SELECT child_count FROM DocSets WHERE id = ?;", (parent_id,))[0]
		if not isinstance(sort_order, int) or sort_order < 0:
			print("Error: Doc creation failed. Invalid sort_order.")
			print("\tsort_order=" + str(sort_order))
			return False
		if sort_order == 0:
			sort_order = parent_child_count + 1
		elif sort_order > parent_child_count + 1:
			sort_order = parent_child_count + 1

		# Execute Insertion
		# Update proceeding doc sort_orders
		self.c.execute("UPDATE Docs SET sort_order = sort_order+1 WHERE sort_order >= ?;", (sort_order))
		# Insert new doc
		self.c.execute("INSERT INTO Docs(extension, parent_id, sort_order) VALUES(?, ?, ?)", (extension, parent_id, sort_order))
		# Update parent child count
		self.c.execute("UPDATE DocSets SET child_count = child_count+1 WHERE id = ?;", (parent_id,))
		self.db.commit()
		return True

	def update(self, id, extension=None, parent_id=None, sort_order=None):
		# Verify id
		if not self.__verifyID(id):
			return False

		# Update extension
		if extension != None:
			if not self.__verifyExtension(extension):
				return False
			self.c.execute("UPDATE Docs SET extension = ? WHERE id = ?;", (extension, id))

		# Update parent_id
		if parent_id != None:
			if sort_order == None:
				print("Error: doc update failed. sort_order must be present to update parent_id.")
				print("\tparent_id=" + str(parent_id))
			# Verify parent_id
			if not self.__verifyParentID(parent_id):
				self.db.rollback()
				return False
			# Execute update
			self.c.execute("UPDATE Tags SET parent_id = ? WHERE id = ?;", (parent_id, id))

		# Update sort_order

		# Commit changes
		self.db.commit()
		return True

	def remove(self, id):
		# Verify id
		if not isinstance(id, int):
			print("Error: Doc removal failed. Invalid id.")
			print("\tid=" + str(id))
			return False 
		
		# Remove all document_tag assignments
		# TODO

		# Execute removal
		self.c.execute("DELETE FROM Docs WHERE id = ?;", (id,))
		self.db.commit()
		return True

	def __verifyID(self, id):
		self.c.execute("SELECT id FROM Docs WHERE id = ? LIMIT 1;", (id,))
		if not isinstance(id, int) or self.c.fetchone() == None:
			print("Error: Doc update failed. Invalid id.")
			print("\tid=" + str(id))
			return False
		return True

	def __verifyExtension(self, extension):
		if not all(c.isdigit() or c.isalpha() or c == "-" for c in extension):
			print("Error: Doc creation failed. Invalid extension.")
			print("\textension=" + str(extension))
			return False
		return True

	def __verifyParentID(self, parent_id):
		self.c.execute("SELECT id FROM DocSets WHERE id = ?;", (parent_id,))
		if not isinstance(parent_id, int) or self.c.fetchone() == None:
			print("Error: Doc creation faield. Invalid parent_id.")
			print("\tparent_id=" + str(parent_id))
			return False
		return True