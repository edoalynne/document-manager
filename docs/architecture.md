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
## Mapping Tables