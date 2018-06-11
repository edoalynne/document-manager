from document_manager.database.repo import Repo

class App:
    def __init__(self):
        pass

    def run(self):
        myRepo = Repo("C:/jcb/my-repo")
        print(myRepo)
        for s in myRepo.documentSets:
            print(s)