from pathlib import Path

from commits import list_commits, timestamp


repo = Path("D:/ProgrammingProjects/suite2p2")

for commit in list_commits(repo=repo)[:3]:
    print(timestamp(repo, commit), commit, sep='\t')

