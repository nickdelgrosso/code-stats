from pathlib import Path

from commits import list_commits


path_name = Path("D:/ProgrammingProjects/suite2p2")

commits = list_commits(repo=path_name)
print(commits)

