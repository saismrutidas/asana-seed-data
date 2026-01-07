import random
from typing import List, Any


def seed_everything(seed: int):
    """
    Seed all randomness for reproducibility.
    """
    random.seed(seed)


def weighted_choice(items: List[Any], weights: List[float]) -> Any:
    """
    Select a single item based on weights.
    """
    return random.choices(items, weights=weights, k=1)[0]


def probability(p: float) -> bool:
    """
    Return True with probability p.
    """
    return random.random() < p
