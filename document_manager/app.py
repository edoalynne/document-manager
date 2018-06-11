from document_manager.database.repo import Repo
from document_manager.database import repo_manager

class App:
    def __init__(self):
        pass

    def run(self):
        myRepo = repo_manager.createRepo("C:\\jcb\\test-repo", "Test Repo", counter=721)
        print(myRepo)