from pathlib import Path
from datetime import datetime
from csv import DictWriter

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



repo = Path("D:/ProgrammingProjects/suite2p2")
max_history = 3

csv_output_file = Path("./stats.csv")
with csv_output_file.open(mode="w", newline="") as f:
    csv_writer = DictWriter(f, fieldnames=[field.name for field in fields(CommitStats)])
    csv_writer.writeheader()
    for commit in tqdm(list_commits(repo=repo)[:max_history], desc="Writing Commits to CSV"):
        checkout(repo, commit)
        python = [stat for stat in count_lines(repo) if stat.language == 'Python'][0]
        stats = CommitStats(
            hash=commit,
            timestamp=timestamp(repo, commit),
            language=python.language,
            files=python.files,
            loc=python.lines_of_code,
            comments=python.comments,
            mean_cyclomatic_complexity=mean_cyclomatic_complexity(repo.joinpath("suite2p"), exclude_pattern="*gui*.py")
        )
        csv_writer.writerow(asdict(stats))