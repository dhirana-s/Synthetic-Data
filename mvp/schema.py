# decides what columns exist and how values are initially sampled.
# it creates raw, messy fake data - doesn't enforce medical logic yet.

import numpy as np

def sample_schema(n, rng):
    return {
        "age": rng.integers(18, 65, size=n),
        "diagnosis": rng.choice(
            ["none", "depression", "anxiety"],
            size=n,
            p=[0.4, 0.35, 0.25]
        ),
        "phq9": rng.integers(0, 28, size=n),
        "gad7": rng.integers(0, 22, size=n),
    }
