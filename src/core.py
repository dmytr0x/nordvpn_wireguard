import sys

from typing import Never


def terminate(msg: str, exit_code: int = 1) -> Never:
    print(msg, file=sys.stderr)  # noqa: T201
    sys.exit(exit_code)
