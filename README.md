# Git Commit History Stats

Get line counts and complexity measurements from a Python package's git repo's history.

## Installation

```
pip install git+https://github.com/nickdelgrosso/code-stats
```


## Minimal Usage

### As a Python package

```python
from pathlib import Path
from code-stats import analyze_history, yield_to_csv

stats_gen = analyze_history(
    repo=Path("D:/ProgrammingProjects/suite2p2/suite2p"),  # Where the python package is located
    max_history=None,  # How far in the past you want to explore
    exclude="*gui*.py",  # A simple grep pattern for excluding certain filenames.
) 
yield_to_csv(stats_gen, Path("./stats_suite2p.csv")) 
```

### As a command-line tool
```
code-stats path/to/repo repo_lines_and_complexity_history.csv
```
