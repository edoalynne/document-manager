import sqlite3

def main():
	db = sqlite3.connect('C:/jcb/repos/test.db')
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
			level INTEGER DEFAULT 0,
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
	c.execute("INSERT INTO Fields(name, type, priority, color) VALUES(?, ?, ?, ?)", ("BlueField", "type1", 3, "0000FF"))
	c.execute("INSERT INTO Fields(name, type, priority, color) VALUES(?, ?, ?, ?)", ("RedField", "type1", 1, "FF0000"))
	c.execute("INSERT INTO Fields(name, type, priority, color) VALUES(?, ?, ?, ?)", ("GreenField", "type1", 2, "00FF00"))
	# Insert Tags
	c.execute("INSERT INTO Tags(value, parent_id) VALUES(?, ?)", ("1", "Pink"))
	c.execute("INSERT INTO Tags(value, parent_id) VALUES(?, ?)", ("1", "Magenta"))
	c.execute("INSERT INTO Tags(value, parent_id) VALUES(?, ?)", ("2", "Lime"))
	c.execute("INSERT INTO Tags(value, parent_id) VALUES(?, ?)", ("2", "Olive"))
	c.execute("INSERT INTO Tags(value, parent_id) VALUES(?, ?)", ("3", "Sky"))
	c.execute("INSERT INTO Tags(value, parent_id) VALUES(?, ?)", ("3", "Cyan"))
	# Insert DocumentSets
	c.execute("INSERT INTO DocumentSets(parent_id, level) VALUES(?, ?)", ("NULL", "0"))
	c.execute("INSERT INTO DocumentSets(parent_id, level) VALUES(?, ?)", (1, "1"))
	c.execute("INSERT INTO DocumentSets(parent_id, level) VALUES(?, ?)", (1, "1"))
	c.execute("INSERT INTO DocumentSets(parent_id, level) VALUES(?, ?)", (3, "2"))
	db.commit()

	c.execute("SELECT level FROM DocumentSets WHERE id = {}".format())
	db.commit()

	db.close()

def insertDocumentSet(parent_id):
	if 

if __name__ == "__main__":
	main()