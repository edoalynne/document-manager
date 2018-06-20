from many_docs_manager.database.repo import Repo

class App:
    def __init__(self):
        pass

    def run(self):
        myRepo = Repo("C:/Jacob/Documents/Projects/_box/", "me reep2")
        print(myRepo)
        myRepo.field.create("Red Field", "strict", 0, "FF0000")
        myRepo.field.create("Green Field", "expandable", 1, "00FF00")
        myRepo.field.create("Blue Field", "strict", 2, "0000FF")
        
        myRepo.tag.create("Fire", 1)
        myRepo.tag.create("Lava", 1)
        myRepo.tag.create("Grass", 2)
        myRepo.tag.create("Tree", 2)
        myRepo.tag.create("Water", 3)
        myRepo.tag.create("Ocean", 3)

        