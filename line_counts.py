from pathlib import Path
from subprocess import Popen, PIPE
from dataclasses import dataclass
from typing import Iterable


@dataclass
class LineCounts:
    language: str
    files: int
    lines_of_code: int
    comments: int


def count_lines(repo: Path) -> Iterable[LineCounts]:
    proc = Popen('pygount suite2p --format=summary', stdout=PIPE, stderr=PIPE,
                 cwd=str(repo))
    lines = proc.stdout.readlines()
    lines = [line.decode().strip() for line in lines]
    header = lines[0]
    code_lines = lines[2:-2]
    for code_line in code_lines:
        stats = {key: val for key, val in zip(header.split(), code_line.split())}
        yield LineCounts(
            language=stats['Language'],
            files=int(stats['Files']),
            lines_of_code=int(stats['Code']),
            comments=int(stats['Comment'])
        )
