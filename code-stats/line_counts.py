from pathlib import Path
from subprocess import Popen, PIPE
from dataclasses import dataclass
from typing import Iterable, Optional

@dataclass
class LineCounts:
    language: str
    files: int
    lines_of_code: int
    comments: int


def count_lines(path: Path, exclude_pattern: Optional[str] = None) -> Iterable[LineCounts]:
    if not path.exists():
        raise FileExistsError("Path does not exist.")
    cmd = f'pygount {str(path)} --format=summary --names-to-skip={exclude_pattern}' if exclude_pattern else f'pygount {str(path)} --format=summary'
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    lines = proc.stdout.readlines()
    lines = [line.decode().strip() for line in lines]
    header = lines[0]
    code_lines = lines[2:-2]
    for code_line in code_lines:
        if len(header.split()) == len(code_line.split()) and 'Text' not in code_line:
            stats = {key: val for key, val in zip(header.split(), code_line.split())}
            yield LineCounts(
                language=stats['Language'],
                files=int(stats['Files']),
                lines_of_code=int(stats['Code']),
                comments=int(stats['Comment'])
            )
