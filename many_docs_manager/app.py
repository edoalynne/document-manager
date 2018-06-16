from many_docs_manager.database.repo import Repo

class App:
    def __init__(self):
        pass

    def run(self):
        myRepo = Repo("C:/Jacob/Documents/Projects/_box/My Repo")
        print(myRepo)