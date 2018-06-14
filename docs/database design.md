# Object Tables
~~~
CREATE TABLE Fields (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	type TEXT,
	priority INTEGER,
	color TEXT
);
~~~
~~~
CREATE TABLE Tags (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	value TEXT,
	parent_id INTEGER,
	FOREIGN KEY(parent_id) REFERENCES Fields(id)
);
~~~
~~~
CREATE TABLE DocumentSets (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	parent_id INTEGER,
	sequence_order INTEGER,
	FOREIGN KEY(parent_id) REFERENCES DocumentSets(id)
);
~~~
~~~
CREATE TABLE Documents (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	extension TEXT,
	parent_id INTEGER,
	FOREIGN KEY(parent_id) REFERENCES DocumentSets(id)
);
~~~

# Mapping Tables
~~~
CREATE TABLE Document_Tag (
	document_id INTEGER,
	tag_id INTEGER,
	FOREIGN KEY(document_id) REFERENCES Documents(id),
	FOREIGN KEY(tag_id) REFERENCES Tags(id)
	PRIMARY KEY(document_id, tag_id)
);
~~~