import xml.etree.ElementTree as ET
import sqlite3
import os

def createRepo(repoPath, name):
    # Fix slashes and add trailing slash
    repoPath.replace("\\", "/")
    if repoPath[-1] != "/":
        repoPath += "/"

    # Ensure file structure is correct
    repoParentPath = repoParentPath[:repoPath[:-1].rfind('/')]
    if not os.path.exists(repoParentPath):
        print("ERROR: Parent path for new repo does not exist.")
        print("\tname=" + name)
        print("\tpath=" + repoPath)
        return False

    if os.path.exists(repoPath):
        print("ERROR: Repo Path for new repo already exists.")
        print("\tname=" + name)
        print("\tpath=" + repoPath)
        return False

    # Create the config file
    configRoot = ET.Element("repo")
    configName = ET.SubElement(configRoot, "name")
    configName.text = name
    configPath = ET.SubElement(configRoot, "path")
    configPath.text = repoPath
    ET.ElementTree(configRoot).write(repoPath + "config.xml")

    # Create the database file
    db = sqlite3.connect(repoPath + "repo.db")
    c = db.cursor()

    # Create tables
    c.execute("CREATE TABLE fields(id TEXT, name TEXT, type TEXT)")
    c.execute("CREATE TABLE tags(id TEXT, value TEXT)")
    db.commit()

    # Insert Config entry
    c.execute("INSERT INTO fields(id, name, type) VALUES(?,?,?)", ("F123", "Cool Field", "Strict"))
    db.commit()
    db.close()

    print("New repo created: " + repoPath)


class Database:
    def __init__(self, databasePath):
        self.conn = sqlite3.connect(databasePath)
        self.c = self.conn.cursor()