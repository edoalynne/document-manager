import sqlite3
import string

def main():
	# C:/Jacob/Documents/Projects/test.db
	db = sqlite3.connect('C:/jcb/repos/test.db')
	c = db.cursor()

	# Construct the repo
	createRepo(db, c)

	# Insert Fields
	createField(db, c, "Red", "Static", 0, "FF0000")
	createField(db, c, "Green", "Extendable", 1, "00FF00")
	createField(db, c, "Blue", "Free", 2, "0000ff")
	# Insert Tags
	createTag(db, c, "Pink", 1)
	createTag(db, c, "Magenta", 1)
	createTag(db, c, "Lime", 2)
	createTag(db, c, "Olive", 2)
	createTag(db, c, "Sky", 3)
	createTag(db, c, "Cyan", 3)
	# Insert DocumentSets
	createDocumentSet(db, c, "NULL")
	createDocumentSet(db, c, 1)
	createDocumentSet(db, c, 2)
	createDocumentSet(db, c, 1)
	createDocumentSet(db, c, "NULL")
	# Insert Documents
	createDocument(db, c, "jpg", 1)
	createDocument(db, c, "png", 2)
	createDocument(db, c, "mp4", 3)
	createDocument(db, c, "wav", 4)
	createDocument(db, c, "mp3", 5)

	# Update Tags
	updateTag(db, c, 6, "CYANUH")
	
	# Remove Fields
	removeField(db, c, 1)
	# Remove Tags
	removeTag(db, c, 3)
	removeTag(db, c, 5)
	# Remove DocumentSets
	removeDocumentSet(db, c, 2)
	# Remove Documents
	removeDocument(db, c, 1)

	db.close()

def createRepo(database, cursor):
	# Object Tables
	cursor.execute('''
		CREATE TABLE Fields (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT,
			type TEXT,
			priority INTEGER,
			color TEXT
		);
	''')
	cursor.execute('''
		CREATE TABLE Tags (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			value TEXT,
			parent_id INTEGER,
			FOREIGN KEY(parent_id) REFERENCES Fields(id)
		);
	''')
	cursor.execute('''
		CREATE TABLE DocumentSets (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			parent_id INTEGER,
			FOREIGN KEY(parent_id) REFERENCES DocumentSets(id)
		);
	''')
	cursor.execute('''
		CREATE TABLE Documents (
			id INTEGER PRIMARY KEY,
			extension TEXT,
			parent_id INTEGER,
			FOREIGN KEY(parent_id) REFERENCES DocumentSets(id)
		);
	''')
	# Mapping Tables
	cursor.execute('''
		CREATE TABLE Document_Tag (
			document_id INTEGER,
			tag_id INTEGER,
			FOREIGN KEY(document_id) REFERENCES Documents(id),
			FOREIGN KEY(tag_id) REFERENCES Tags(id)
			PRIMARY KEY(document_id, tag_id)
		);
	''')
	database.commit()

def createField(database, cursor, name, type, priority, color):
	# verify name
	if not isinstance(name, str) or \
			not all(c.isdigit() or c.isalpha() or c.isspace() for c in name):
		print("ERROR: Could not create field. Invalid name: " + str(name))
		return False

	# verify type
	if not isinstance(type, str):
		print("ERROR: Could not create field. Invalid type: " + str(type))
		return False

	# verify priority
	if not isinstance(priority, int) or \
			priority < 0:
		print("ERROR: Could not create field. Invalid priority: " + str(priority))
		return False

	# verify color
	if not isinstance(color, str) or \
			not len(color) == 6 or \
			not all(c in string.hexdigits for c in color):
		print("ERROR: Could not create field. Invalid color: " + str(color))
		return False

	cursor.execute("INSERT INTO Fields(name, type, priority, color) VALUES(?, ?, ?, ?)", (name, type, priority, color))
	database.commit()

def updateField(database, cursor, id, name=None, type=None, priority=None, color=None):
	pass

def removeField(database, cursor, id):
	# Remove all tags belonging to the field
	cursor.execute("SELECT id FROM Tags WHERE parent_id = ?", (id,))
	for tag_id in cursor.fetchall():
		removeTag(database, cursor, tag_id[0])
	# Remove the field
	cursor.execute("DELETE FROM Fields WHERE id = ?", (id,))
	print("REMOVED: Field with id=" + str(id))
	database.commit()

def createTag(database, cursor, value, parent_id):
	# verify value
	if not isinstance(value, str) or \
			not all(c.isdigit() or c.isalpha() or c == "-" for c in value):
		print("ERROR: Could not create tag. Invalid value: " + str(value))
		return False

	# verify parent_id
	cursor.execute("SELECT id FROM Fields WHERE id = ?;", (parent_id,))
	if not isinstance(parent_id, int) or cursor.fetchone() == None:
		print("ERROR: Could not create tag. Invalid parent_id: " + str(parent_id))
		return False

	cursor.execute("INSERT INTO Tags(value, parent_id) VALUES(?, ?);", (value, parent_id))
	database.commit()

def updateTag(database, cursor, id, value=None, parent_id=None):
	if not value == None:
		# verify value
		if not isinstance(value, str) or \
				not all(c.isdigit() or c.isalpha() or c == "-" for c in value):
			print("ERROR: Could not create tag. Invalid value: " + str(value))
			return False

		cursor.execute("UPDATE Tags SET value = ? WHERE id = ?", (value, id))
		print("UPDATED: Tag with id=" + str(id))
		database.commit()

def removeTag(database, cursor, id):
	# verify id
	if not isinstance(id, int):
		print("ERROR: Could not remove tag. Invalid id: " + str(id))
		return False
	# Remove all document tag assignments
	cursor.execute("DELETE FROM Document_Tag WHERE tag_id = ?", (id,))
	# Remove the tag
	cursor.execute("DELETE FROM Tags WHERE id = ?", (id,))
	print("REMOVED: Tag with id=" + str(id))
	database.commit()

def createDocumentSet(database, cursor, parent_id):
	# verify parent_id
	if parent_id != "NULL":
		cursor.execute("SELECT id FROM DocumentSets WHERE id = ?;", (parent_id,))
		if not isinstance(parent_id, int) or cursor.fetchone() == None:
			print("ERROR: Could not create Document Set. Invalid parent_id: " + str(parent_id))
			return False

	cursor.execute("INSERT INTO DocumentSets(parent_id) VALUES(?);", (parent_id,))
	database.commit()

def updatedocumentSet(database, cursor, id, parent_id=None):
	pass

def removeDocumentSet(database, cursor, id):
	# Remove all child document sets
	cursor.execute("SELECT id FROM DocumentSets WHERE parent_id = ?", (id,))
	for document_set_id in cursor.fetchall():
		removeDocumentSet(database, cursor, document_set_id[0])
	# Remove all child documents
	cursor.execute("SELECT id FROM Documents WHERE parent_id = ?", (id,))
	for document_id in cursor.fetchall():
		removeDocument(database, cursor, document_id[0])
	# Remove the document set
	cursor.execute("DELETE FROM DocumentSets WHERE id = ?", (id,))
	print("REMOVED: Document Set with id=" + str(id))
	database.commit()

def createDocument(database, cursor, extension, parent_id):
	# verify extension
	if not isinstance(extension, str) or \
			not all(c.isalpha() or c.isdigit() for c in extension):
		print("ERROR: Could not create Document. Invalid extension: " + str(extension))
		return False

	# verify parent_id
	if not parent_id == "NULL":
		cursor.execute("SELECT id FROM DocumentSets WHERE id = ?;", (parent_id,))
		if not isinstance(parent_id, int) or cursor.fetchone() == None:
			print("ERROR: Could not create Document. Invalid parent_id: " + str(parent_id))
			return False
	
	cursor.execute("INSERT INTO Documents(extension, parent_id) VALUES(?, ?);", (extension, parent_id))
	database.commit()

def updateDocument(database, cursor, id, parent_id=None, extension=None):
	pass

def removeDocument(database, cursor, id):
	# Remove document tag assignments
	cursor.execute("DELETE FROM Document_Tag WHERE document_id = ?", (id,))
	# Remove the document
	cursor.execute("DELETE FROM Documents WHERE id = ?", (id,))
	print("REMOVED: Document with id=" + str(id))
	database.commit()

if __name__ == "__main__":
	main()