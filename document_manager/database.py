import xml.etree.ElementTree as ET
import sqlite3
import os

def createRepo(repoPath, name):
    # Fix slashes and add trailing slash
    repoPath = repoPath.replace("\\", "/")
    if repoPath[-1] != "/":
        repoPath += "/"

    # Ensure file structure is correct
    repoParentPath = repoPath[:repoPath[:-1].rfind('/')]
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

    # Create the directory
    os.mkdir(repoPath)

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
    c.execute("CREATE TABLE Fields(FieldID INTEGER, Name TEXT, Type TEXT)")
    c.execute("CREATE TABLE Tags(TagID INTEGER, Value TEXT)")
    c.execute("CREATE TABLE TagAssignments(TagAssignmentID TEXT, FieldID INTEGER, TagID INTEGER)")
    db.commit()

    # Insert Config entry
    c.execute("INSERT INTO Fields(FieldID, Name, Type) VALUES(?,?,?)", (0, "Cool Field", "Strict"))
    c.execute("INSERT INTO Fields(FieldID, Name, Type) VALUES(?,?,?)", (1, "Nice Field", "Loose"))
    c.execute("INSERT INTO Tags(TagID, Value) VALUES(?,?)", (0, "Hot Tag"))
    c.execute("INSERT INTO Tags(TagID, Value) VALUES(?,?)", (1, "Cold Tag"))
    c.execute("INSERT INTO Tags(TagID, Value) VALUES(?,?)", (2, "Warm Tag"))
    c.execute("INSERT INTO Tags(TagID, Value) VALUES(?,?)", (3, "Chilly Tag"))
    c.execute("INSERT INTO TagAssignments(TagAssignmentID, FieldID, TagID) VALUES(?,?,?)", (0, 0, 1))
    c.execute("INSERT INTO TagAssignments(TagAssignmentID, FieldID, TagID) VALUES(?,?,?)", (1, 0, 3))
    c.execute("INSERT INTO TagAssignments(TagAssignmentID, FieldID, TagID) VALUES(?,?,?)", (2, 1, 0))
    c.execute("INSERT INTO TagAssignments(TagAssignmentID, FieldID, TagID) VALUES(?,?,?)", (3, 1, 2))
    db.commit()
    db.close()

    print("New repo created: " + repoPath)