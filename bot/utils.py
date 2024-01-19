from abc import ABC
from pathlib import Path
from typing import Final


class PathControl(ABC):
    """Get path relative to project root"""

    ROOT: Final[Path] = Path(__file__).parent.parent

    @classmethod
    def get(cls, path: str | Path) -> Path:
        return cls.ROOT.joinpath(path)
