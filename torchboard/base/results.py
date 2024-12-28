from dataclasses import dataclass
from typing import List


@dataclass
class Results:
    acc: List[float]
    loss: List[float]
