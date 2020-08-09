from pathlib import Path

from commits import list_commits, timestamp, checkout
from line_counts import count_lines

repo = Path("D:/ProgrammingProjects/suite2p2")

for commit in list_commits(repo=repo)[:3]:
    checkout(repo, commit)
    time = timestamp(repo, commit)
    lines = [stat for stat in count_lines(repo) if stat.language == 'Python']
    print(commit, time, lines)