from pathlib import Path
from datetime import datetime
from csv import DictWriter
from typing import Optional, Iterable
from tqdm import tqdm

from commits import list_commits, timestamp, checkout
from line_counts import count_lines
from dataclasses import dataclass, asdict, fields
from cyclomatic_complexity import mean_cyclomatic_complexity


@dataclass
class CommitStats:
    hash: str
    timestamp: datetime
    language: str
    files: int
    loc: int
    comments: int
    mean_cyclomatic_complexity: float


def analyze_history(repo: Path, max_history: Optional[int] = None, exclude: Optional[str] = None) -> Iterable[CommitStats]:
    """Yields a Python CommitStats object for each commit in the repo's history."""
    commits = list_commits(repo=repo)
    if max_history:
        commits = commits[:max_history]
    for commit in tqdm(commits, desc="Writing Commits to CSV"):
        checkout(repo, commit)
        python = [stat for stat in count_lines(repo, exclude_pattern=exclude) if stat.language == 'Python'][0]
        yield CommitStats(
            hash=commit,
            timestamp=timestamp(repo, commit),
            language=python.language,
            files=python.files,
            loc=python.lines_of_code,
            comments=python.comments,
            mean_cyclomatic_complexity=mean_cyclomatic_complexity(repo, exclude_pattern=exclude)
        )



if __name__ == '__main__':

    repo = Path("D:/ProgrammingProjects/suite2p2/suite2p")
    max_history = None #30
    exclude = "*gui*.py"
    csv_output_file = Path("./stats2.csv")

    with csv_output_file.open(mode="w", newline="") as f:
        csv_writer = DictWriter(f, fieldnames=[field.name for field in fields(CommitStats)])
        csv_writer.writeheader()
        for stats in analyze_history(repo=repo, max_history=max_history, exclude=exclude):
            csv_writer.writerow(asdict(stats))
