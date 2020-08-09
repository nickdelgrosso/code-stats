__all__ = ['CommitHash', 'list_commits']

from typing import NewType, List
from pathlib import Path
from subprocess import Popen, PIPE

CommitHash = NewType("CommitHash", str)


def list_commits(repo: Path) -> List[CommitHash]:
    proc = Popen('git rev-list --all', stdout=PIPE, stderr=PIPE, cwd=str(repo))
    commit_hashes = [commit.decode().strip() for commit in proc.stdout.readlines()]
    commit_hashes = [CommitHash(commit) for commit in commit_hashes]
    return commit_hashes

