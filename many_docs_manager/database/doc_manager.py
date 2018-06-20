import sqlite3

class DocManager:
	def __init__(self, database, cursor):
		self.db = database
		self.c = cursor

	def create(self, extension, parent_id, sort_order=0):
		# Verify extension
		if not all(c.isdigit() or c.isalpha() or c == "-" for c in extension):
			print("Error: Doc creation failed. Invalid extension.")
			print("\textension=" + str(extension))
			return False
	
		# Verify parent_id
		self.c.execute("SELECT id FROM DocSets WHERE id = ?;", (parent_id,))
		if not isinstance(parent_id, int) or self.c.fetchone() == None:
			print("Error: Doc creation faield. Invalid parent_id.")
			print("\tparent_id=" + str(parent_id))
			return False

		# Verify sort_order
		if not isinstance(sort_order, int) or sort_order < 0:
			print("Error: Doc creation failed. Invalid sort_order.")
			print("\tsort_order=" + str(sort_order))
			return False
		if sort_order == -1:
			# TODO Insert into end
		else:
			# TODO who bloody knows

		# Execute Insertion
		self.c.execute("INSERT INTO Docs(extension, parent_id, sort_order) VALUES(?, ?, ?)", (extension, parent_id, sort_order))
		self.db.commit()
		return True

	def update(self, id, extension=None, parent_id=None, sort_order=None):
		# Verify id
		self.c.execute("SELECT id FROM Docs WHERE id = ? LIMIT 1;", (id,))
		if not isinstance(id, int) or self.c.fetchone() == None:
			print("Error: Doc update failed. Invalid id.")
			print("\tid=" + str(id))
			return False

		# Update extension
		if extension != None:
			# Verify extension
			if not isinstance(extension, str) or not all(c.isdigit() or c.isalpha() or c == "-" for c in extension):
				print("Error: Doc update failed. Invalid extension.")
				print("\textension=" + str(extension))
				self.db.rollback()
				return False
			# Execute update
			self.c.execute("UPDATE Docs SET extension = ? WHERE id = ?;", (extension, id))

		# Update parent_id
		if parent_id != None:
			# Verify parent_id
			self.c.execute("SELECT id FROM Fields WHERE id = ? LIMIT 1;", (parent_id,))
			if not isinstance(parent_id, int) or self.c.fetchone() == None:
				print("Error: Tag update failed. Invalid parent_id.")
				print("\tparent_id=" + str(parent_id))
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