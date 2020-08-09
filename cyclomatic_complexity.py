from typing import Optional
from pathlib import Path
from subprocess import Popen, PIPE

def mean_cyclomatic_complexity(path: Path, exclude_pattern: Optional[str] = None) -> float:
    cmd = f'radon cc {path} -a --exclude={exclude_pattern}' if exclude_pattern else f'radon cc {path} -a'
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    lines = proc.stdout.readlines()
    last_line = lines[-2].strip().decode()
    cc = float(last_line.split('(')[-1].split(')')[0])
    return cc


