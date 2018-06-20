# Repo
## File Structure
```
/repo-name
    /documents
        [document-id].[extension]
    config.xml
    repo.db
```
# Database
## Object Tables
```
CREATE TABLE Fields (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    vocab TEXT,
    priority INTEGER,
    color TEXT
);
```
```
CREATE TABLE Tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value TEXT,
    parent_id INTEGER,
    FOREIGN KEY(parent_id) REFERENCES Fields(id)
);
```
```
CREATE TABLE Docs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    extension TEXT,
    parent_id INTEGER,
    sort_order INTEGER,
    FOREIGN KEY(parent_id) REFERENCES DocSets(id)
);
```
```
CREATE TABLE DocSets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id INTEGER,
    sort_order INTEGER,
    child_count INTEGER,
    FOREIGN KEY(parent_id) REFERENCES DocSets(id)
);
```
## Mapping Tables