import subprocess as shell

branchName = input("Branch Name: ")
commitName = input("Commit Name: ")

commitSentence = "git commit -m \"" + commitName + "\""

shell.call("git add .", shell=True)
shell.call(commitSentence, shell=True)
shell.call("git push -u origin " + branchName, shell=True)
