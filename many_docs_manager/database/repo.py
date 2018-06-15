from many_docs_manager.database.field_manager import FieldManager
from many_docs_manager.database.tag_manager import TagManager

import os
import sqlite3

class Repo:
    def __init__(self, path, name=None):
        self.name = 0
        self.db = 0
        self.c = 0
        self.field = 0
        self.tag = 0

        # If name is not set, create a new repo
        if name != None:
            self.__create(path, name)

        # If name is set, load an existing repo
        else:
            self.__load(path)

    def __create(self, path, name):
        # Verify name and path
        # TODO

        # Create directories
        os.mkdir(path)
        os.mkdir(path + "documents")

        # Create configuration
        # TODO

        # Create database and get cursor
        self.db = sqlite3.connect(path + "repo.db")
        self.c = self.db.cursor()

        # Create tables
        # TODO

        # Create managers
        self.field = FieldManager(self.db, self.c)
        self.tag = TagManager(self.db, self.c)

    def __load(self, path):
        # Verify path
        # TODO

        # Connect to database and get cursor
        self.db = sqlite3.connect(path + "repo.db")
        self.c = self.db.cursor()

        # Create managers
        self.field = FieldManager(self.db, self.c)
        self.tag = TagManager(self.db, self.c)