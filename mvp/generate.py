# the tool to wire everything together and produce a csv. 

import argparse
import numpy as np
import pandas as pd

from schema import sample_schema
from constraints import apply_constraints


def main(n, output, seed): #seed controls randomness (same seed -> same data)
    rng = np.random.default_rng(seed) #creates a random generators ensuring reproducibility

    data = sample_schema(n, rng)
    data = apply_constraints(data)

    df = pd.DataFrame(data) # converts dictionary to table
    df.to_csv(output, index=False)

    print(f"Generated {n} rows → {output}")


# CLI entry point
if __name__ == "__main__":  # means only run this if user executes the file directly
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=10000)
    parser.add_argument("--output", type=str, default="synthetic.csv")
    parser.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()
    main(args.rows, args.output, args.seed)
