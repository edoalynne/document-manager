from document_manager.database import createRepo

class App:
    def run(self):
        repoName = input("Enter new repo name: ")
        while not all(x.isdigit() or x.isalpha() or x.isspace() for x in repoName):
            print("Invalid repo name. Only use digits, numbers, and spaces.")
            repoName = input("Enter new repo name: ")

        repoPath = "C:\\Jacob\\Documents\\Projects\\" + repoName.lower().replace(" ", "-")
        createRepo(repoPath, "My Repo2")