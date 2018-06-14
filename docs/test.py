import sqlite3
import string

def main():
	# C:/Jacob/Documents/Projects/test.db
	db = sqlite3.connect('C:/Jacob/Documents/Projects/test.db')
	c = db.cursor()

	#### TABLE CREATION
	########################
	# Object Tables
	c.execute('''
		CREATE TABLE Fields (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT,
			type TEXT,
			priority INTEGER,
			color TEXT
		);
	''')
	c.execute('''
		CREATE TABLE Tags (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			value TEXT,
			parent_id INTEGER,
			FOREIGN KEY(parent_id) REFERENCES Fields(id)
		);
	''')
	c.execute('''
		CREATE TABLE DocumentSets (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			parent_id INTEGER,
			FOREIGN KEY(parent_id) REFERENCES DocumentSets(id)
		);
	''')
	c.execute('''
		CREATE TABLE Documents (
			id INTEGER PRIMARY KEY,
			extension TEXT,
			parent_id INTEGER,
			FOREIGN KEY(parent_id) REFERENCES DocumentSets(id)
		);
	''')
	# Mapping Tables
	c.execute('''
		CREATE TABLE Document_Tag (
			document_id INTEGER,
			tag_id INTEGER,
			FOREIGN KEY(document_id) REFERENCES Documents(id),
			FOREIGN KEY(tag_id) REFERENCES Tags(id)
			PRIMARY KEY(document_id, tag_id)
		);
	''')
	db.commit()

	#### ENTRY INSERTIONS
	########################
	# Insert Fields
	createField(db, c, "Red", "Static", 0, "FF0000")
	createField(db, c, "Green", "Extendable", 1, "00FF00")
	createField(db, c, "Blue", "Free", 2, "0000ff")
	# Insert Tags
	createTag(db, c, "Pink", 1)
	createTag(db, c, "Magenta", 1)
	createTag(db, c, "Lime", 2)
	createTag(db, c, "Olive", 2)
	createTag(db, c, "Sky", 6)
	createTag(db, c, "Cyan", 3)
	# # Insert DocumentSets
	# c.execute("INSERT INTO DocumentSets(parent_id) VALUES(?, ?)", ("NULL"))
	# c.execute("INSERT INTO DocumentSets(parent_id) VALUES(?, ?)", (1))
	# c.execute("INSERT INTO DocumentSets(parent_id) VALUES(?, ?)", (1))
	# c.execute("INSERT INTO DocumentSets(parent_id) VALUES(?, ?)", (3))
	# db.commit()

	db.close()

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

def createTag(database, cursor, value, parent_id):
	# verify value
	if not isinstance(value, str) or \
			not all(c.isdigit() or c.isalpha() or c == "-" for c in value):
		print("ERROR: Could not create tag. Invalid value: " + str(value))
		return False

	# verify parent_id
	cursor.execute("SELECT id FROM Fields WHERE id = ?;", (parent_id,))
	qResult = cursor.fetchone()
	if not isinstance(parent_id, int) or \
			qResult == None:
		print("ERROR: Could not create tag. Invalid parent_id: " + str(parent_id))
		return False

	cursor.execute("INSERT INTO Tags(value, parent_id) VALUES(?, ?)", (value, parent_id))
	database.commit()

def createDocumentSet():
	pass

def createDocument():
	pass


if __name__ == "__main__":
	main()