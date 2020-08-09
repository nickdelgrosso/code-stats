from pathlib import Path
from datetime import datetime
from csv import DictWriter
from typing import Optional, Iterable
from dataclasses import dataclass, asdict, fields

from tqdm import tqdm

from .commits import list_commits, timestamp, checkout
from .line_counts import count_lines
from .cyclomatic_complexity import mean_cyclometric_complexity


@dataclass
class CommitStats:
    hash: str
    timestamp: datetime
    language: str
    files: int
    loc: int
    comments: int
    mean_cyclometric_complexity: float


def analyze_history(repo: Path, max_history: Optional[int] = None, exclude: Optional[str] = None) -> Iterable[CommitStats]:
    """Yields a Python CommitStats object for each commit in the repo's history."""
    commits = list_commits(repo=repo)
    if max_history:
        commits = commits[:max_history]
    for commit in tqdm(commits, desc="Writing Commits to CSV"):
        checkout(repo, commit)
        line_counts = count_lines(repo, exclude_pattern=exclude)
        print(line_counts)
        python = [stat for stat in line_counts if stat.language == 'Python']
        if len(python) > 0:
            yield CommitStats(
                hash=commit,
                timestamp=timestamp(repo, commit),
                language=python.language,
                files=python.files,
                loc=python.lines_of_code,
                comments=python.comments,
                mean_cyclometric_complexity=mean_cyclometric_complexity(repo, exclude_pattern=exclude)
            )


def yield_to_csv(stats_gen: Iterable[CommitStats], csv_filename: str) -> None:
    with csv_filename.open(mode="w", newline="") as f:
        csv_writer = DictWriter(f, fieldnames=[field.name for field in fields(CommitStats)])
        csv_writer.writeheader()
        for stats in stats_gen:
            csv_writer.writerow(asdict(stats))


if __name__ == '__main__':

    stats_gen = analyze_history(
        repo=Path("D:/ProgrammingProjects/suite2p2/suite2p"),
        max_history=None, exclude="*gui*.py")
    yield_to_csv(stats_gen, Path("./stats_suite2p.csv"))
