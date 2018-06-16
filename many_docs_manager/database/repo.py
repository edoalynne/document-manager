from many_docs_manager.database.field_manager import FieldManager
from many_docs_manager.database.tag_manager import TagManager

import os
import sqlite3
from xml.etree import ElementTree

class Repo:
    def __init__(self, path, name=None):
        self.name = None
        self.db = None
        self.c = None
        self.field = None
        self.tag = None

        # If name parameter is set, create a new repo
        if name != None:
            self.__create(path, name)

        # If name parameter is not set, load an existing repo
        else:
            self.__load(path)

    def __str__(self):
        return "name:" + str(self.name)

    def __create(self, parent_path, name):
        # Verify parent_path
        parent_path = parent_path.replace("\\", "/")
        if parent_path[-1] != "/":
            parent_path += "/"
        if not os.path.exists(parent_path):
            print("Error: Repo creation failed, parent_path invalid.")
            print("\tparent_path=" + parent_path)
            return False

        # Verify name
        if not all(c.isdigit() or c.isalpha() or c.isspace() for c in name) or \
                not name[0].isalpha() or name[-1].isspace():
            print("Error: Repo creation faild, name invalid.")
            print("\tname=" + name)
            return False
        self.name = name

        # Create directories
        os.mkdir(parent_path + name)
        os.mkdir(parent_path + name + "/documents")

        # Create configuration
        configRoot = ElementTree.Element("repo")
        configName = ElementTree.SubElement(configRoot, "name")
        configName.text = name
        configPath = ElementTree.SubElement(configRoot, "path")
        configPath.text = parent_path + name
        ElementTree.ElementTree(configRoot).write(parent_path + name + "/config.xml")

        # Create database and get cursor
        self.db = sqlite3.connect(parent_path + name + "/repo.db")
        self.c = self.db.cursor()

        # Create tables
        self.c.execute('''
            CREATE TABLE Fields (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                vocab TEXT,
                priority INTEGER,
                color TEXT
            );
        ''')
        self.c.execute('''
            CREATE TABLE Tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                value TEXT,
                parent_id INTEGER,
                FOREIGN KEY(parent_id) REFERENCES Fields(id)
            );
        ''')

        # Create managers
        self.field = FieldManager(self.db, self.c)
        self.tag = TagManager(self.db, self.c)

    def __load(self, path):
        # Verify path
        path = path.replace("\\", "/")
        if path[-1] != "/":
            path += "/"
        if not os.path.exists(path) or not os.path.exists(path + "/documents"):
            print("Error: Repo load failed, path invalid.")
            print("\tpath=" + path)
            return False
        if not os.path.isfile(path + "repo.db"):
            print("Error: Repo load failed, missing database.")
            print("\tpath=" + path)
            return False
        if not os.path.isfile(path + "config.xml"):
            print("Error: Repo load failed, missing configuration.")
            print("\tpath=" + path)
            return False

        # Load configuration
        config = ElementTree.parse(path + "config.xml").getroot()
        for child in config:
            if child.tag == "name":
                self.name = child.text

        # Connect to database and get cursor
        self.db = sqlite3.connect(path + "repo.db")
        self.c = self.db.cursor()

        # Create managers
        self.field = FieldManager(self.db, self.c)
        self.tag = TagManager(self.db, self.c)