import sys
from typing import Never


def terminate(msg: str, exit_code: int = 1) -> Never:
    print(msg, file=sys.stderr)
    exit(exit_code)
