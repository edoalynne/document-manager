import sqlite3

def main():
	db = sqlite3.connect('C:/Jacob/Documents/Projects/test.db')
	c = db.cursor()

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
			value TEXT
		);
	''')
	c.execute('''
		CREATE TABLE DocumentSets (
			id INTEGER PRIMARY KEY AUTOINCREMENT
		);
	''')
	c.execute('''
		CREATE TABLE Documents (
			id INTEGER PRIMARY KEY,
			extension TEXT
		);
	''')
	db.commit()

	# Mapping Tables
	c.execute('''
		CREATE TABLE Field_Tag (
			field_id INTEGER,
			tag_id INTEGER,
			FOREIGN KEY(field_id) REFERENCES Fields(id),
			FOREIGN KEY(tag_id) REFERENCES Tags(id),
			PRIMARY KEY(field_id, tag_id)
		);
	''')
	c.execute('''
		CREATE TABLE Document_Tag (
			document_id INTEGER,
			tag_id INTEGER,
			FOREIGN KEY(document_id) REFERENCES Documents(id),
			FOREIGN KEY(tag_id) REFERENCES Tags(id)
			PRIMARY KEY(document_id, tag_id)
		);
	''')
	c.execute('''
		CREATE TABLE DocumentSet_Document (
			parent_id INTEGER,
			document_id INTEGER,
			FOREIGN KEY(parent_id) REFERENCES DocumentSets(id),
			FOREIGN KEY(document_id) REFERENCES Documents(id),
			PRIMARY KEY(parent_id, document_id)
		);
	''')
	c.execute('''
		CREATE TABLE DocumentSet_DocumentSet (
			parent_id INTEGER,
			child_id INTEGER,
			FOREIGN KEY(parent_id) REFERENCES DocumentSets(id),
			FOREIGN KEY(child_id) REFERENCES DocumentSets(id),
			PRIMARY KEY(parent_id, child_id)
		);
	''')
	db.commit()

	db.close()

if __name__ == "__main__":
	main()