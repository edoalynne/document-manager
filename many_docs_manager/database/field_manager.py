from many_docs_manager.database.tag_manager import TagManager

import string
import sqlite3

class FieldManager:
	def __init__(self, database, cursor, tag_manager):
		self.db = database
		self.c = cursor
		self.tag_manager = tag_manager

	def create(self, name, vocab, priority, color):
		# Verify name
		if not all(c.isdigit() or c.isalpha() or c.isspace() for c in name) or \
				not name[0].isalpha() or name[-1].isspace():
			print("Error: Field creation failed. Invalid name.")
			print("\tname=" + str(name))
			return False
	
		# Verify vocab
		if not isinstance(vocab, str):
			print("Error: Field creation failed. Invalid vocab.")
			print("\tvocab=" + str(vocab))
			return False

		# Verify priority
		if not isinstance(priority, int) or priority < 0:
			print("Error: Field creation failed. Invalid priority.")
			print("\tpriority=" + str(priority))
			return False

		# Verify color
		if not isinstance(color, str) or not len(color) == 6 or \
			not all(c in string.hexdigits for c in color):
			print("Error: Field creation failed. Invalid color.")
			print("\tcolor=" + str(color))
			return False

		# Execute Insertion
		self.c.execute("INSERT INTO Fields(name, vocab, priority, color) VALUES(?, ?, ?, ?)", (name, vocab, priority, color))
		self.db.commit()
		return True

	def update(self, id, name=None, vocab=None, priority=None, color=None):
		# Verify id
		self.c.execute("SELECT id FROM Fields WHERE id = ? LIMIT 1;", (id,))
		if not isinstance(id, int) or self.c.fetchone() == None:
			print("Error: Field update failed. Invalid id.")
			print("\tid=" + str(id))
			return False

		# Update name
		if name != None:
			# Verify name
			if not all(c.isdigit() or c.isalpha() or c.isspace() for c in name) or \
				not name[0].isalpha() or name[-1].isspace():
				print("Error: Field update failed. Invalid name.")
				print("\tname=" + str(name))
				self.db.rollback()
				return False
			# Execute update
			self.c.execute("UPDATE Fields SET name = ? WHERE id = ?;", (name, id))

		# Update vocab
		if vocab != None:
			# Verify vocab
			if not isinstance(vocab, str):
				print("Error: Field update failed. Invalid vocab.")
				print("\tvocab=" + str(vocab))
				self.db.rollback()
				return False
			# Execute update
			self.c.execute("UPDATE Fields SET vocab = ? WHERE id = ?;", (vocab, id))

		# Update priority
		if priority != None:
			# Verify priority
			if not isinstance(priority, int) or priority < 0:
				print("Error: Field update failed. Invalid priority.")
				print("\tpriority=" + str(priority))
				self.db.rollback()
				return False
			# Execute update
			self.c.execute("UPDATE Fields SET priority = ? WHERE id = ?;", (priority, id))

		# Update color
		if color != None:
			# Verify color
			if not isinstance(color, str) or not len(color) == 6 or \
					not all(c in string.hexdigits for c in color):
				print("Error: Tag update failed. Invalid color.")
				print("\tcolor=" + str(color))
				self.db.rollback()
				return False
			# Execute update
			self.c.execute("UPDATE Fields SET color = ? WHERE id = ?;", (color, id))

		# Commit changes
		self.db.commit()
		return True

	def remove(self, id):
		# Verify id
		if not isinstance(id, int):
			print("Error: Field removal failed. Invalid id.")
			print("\tid=" + str(id))
			return False 
		
		# Remove all child tags
		self.c.execute("SELECT id FROM Tags WHERE parent_id = ?;", (id,))
		for tag_id in self.c.fetchall():
			self.tag_manager.remove(tag_id[0])

		# Execute removal
		self.c.execute("DELETE FROM Fields WHERE id = ?;", (id,))
		self.db.commit()
		return True