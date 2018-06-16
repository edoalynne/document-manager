class TagManager:
    def __init__(self, database, cursor):
        self.db = database
        self.c = cursor

    def create(self, value, parent_id):
        # Verify value
        if not all(c.isdigit() or c.isalpha() or c == "-" for c in value) or \
                not c[0].isalpha() or c[-1] == "-":
            print("Error: Tag creation failed. Invalid value.")
            print("\tvalue=" + value)
            return False
    
        # Verify parent_id
        self.c.execute("SELECT id FROM Fields WHERE id = ?;", (parent_id,))
        if not isinstance(parent_id, int) or self.c.fetchone == None:
            print("Error: Tag creation faield. Invalid parent_id.")
            print("\tparent_id=" + parent_id)
            return False

        # Execute Insertion
        self.c.execute("INSERT INTO Tags(value, parent_id) VALUES(?, ?)", (value, parent_id))
        self.db.commit()
        return True

    def update(self, id, value=None, parent_id=None):
        # Verify id
        self.c.execute("SELECT id FROM Tags WHERE id = ? LIMIT 1;", (id,))
        if not isinstance(id, int) or self.c.fetchone() == None:
            print("Error: Tag update failed. Invalid id.")
            print("\tid=" + id)
            return False

        # Update value
        if value != None:
            # Verify value
            if not isinstance(value, str) or not c[0].isalpha() or c[-1] == "-" or \
                    not all(c.isdigit() or c.isalpha() or c == "-" for c in value):
                print("Error: Tag update failed. Invalid value.")
                print("\tvalue=" + value)
                self.db.rollback()
                return False
            # Execute update
            self.c.execute("UPDATE Tags SET value = ? WHERE id = ?;", (value, id))

        # Update parent_id
        if parent_id != None:
            # Verify parent_id
            self.c.execute("SELECT id FROM Fields WHERE id = ? LIMIT 1;", (id,))
            if not isinstance(parent_id, int) or self.c.fetchone() == None:
                print("Error: Tag update failed. Invalid parent_id.")
                print("\tparent_id=" + parent_id)
                self.db.rollback()
                return False
            # Execute update
            self.c.execute("UPDATE Tags SET parent_id = ? WHERE id = ?;", (parent_id, id))

        # Commit changes
        self.db.commit()
        return True

    def remove(self, id):
        # Verify id
        if not isinstance(id, int):
            print("Error: Tag removal failed. Invalid id.")
            print("\tid=" + id)
            return False 
        
        # Remove all document_tag assignments
        # TODO

        # Execute tag removal
        self.c.execute("DELETE FROM Tags WHERE id = ?;", (id,))
        self.db.commit()
        return True