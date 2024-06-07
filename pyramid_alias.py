from argparse import ArgumentParser
from pathlib import Path

import numpy as np


class AliasedDistribution:
    """A class to generate samples from a distribution using the alias method."""

    def __init__(self, counts, prng=None):
        # TODO, consider int64 or uint64 if using global population
        alias = np.full(len(counts), -1, dtype=np.int64)
        probs = np.array(counts, dtype=np.int64)
        total = probs.sum()
        probs *= len(probs)  # TODO, explain this...
        small = [i for i, value in enumerate(probs) if value < total]
        large = [i for i, value in enumerate(probs) if value > total]
        while small:
            ismall = small.pop()
            ilarge = large.pop()
            alias[ismall] = ilarge
            probs[ilarge] -= total - probs[ismall]
            if probs[ilarge] < total:
                small.append(ilarge)
            elif probs[ilarge] > total:
                large.append(ilarge)

        self._alias = alias
        self._probs = probs
        self._total = total

        self._prng = prng if prng else np.random.default_rng()

        return

    @property
    def alias(self):
        return self._alias

    @property
    def probs(self):
        return self._probs

    @property
    def total(self):
        return self._total

    def sample(self, count=1):
        """Generate samples from the distribution."""

        if count == 1:
            i = self._prng.integers(low=0, high=len(self._alias))
            d = self._prng.integers(low=0, high=self._total)

            i = i if d < self._probs[i] else self._alias[i]
        else:
            i = self._prng.integers(low=0, high=len(self._alias), size=count)
            d = self._prng.integers(low=0, high=self._total, size=count)
            a = d >= self._probs[i]
            i[a] = self._alias[i[a]]

        return i


def load_pyramid_csv(file: Path, quiet=False):
    """Load a CSV file with population pyramid data."""

    if not quiet:
        print(f"Reading data from '{file}' ...")
    # Expected file schema:
    # "Age,M,F"
    # "low-high,#males,#females"
    # ...
    # "max+,#males,#females"
    with file.open("r") as f:
        # Use strip to remove newline characters
        lines = [line.strip() for line in f.readlines()]
    text = lines[1:]  # Skip the first line
    text = [line.split(",") for line in text]  # Split each line by comma
    # Split the first element by hyphen
    text = [line[0].split("-") + line[1:] for line in text]
    # Remove the plus sign from the last element
    text[-1][0] = text[-1][0].replace("+", "")
    data = [list(map(int, line)) for line in text]  # Convert all elements to integers
    data[-1] = [
        data[-1][0],
        data[-1][0],
        *data[-1][1:],
    ]  # Make the last element a single year bucket

    datanp = np.zeros((len(data), 5), dtype=np.int64)
    for i, line in enumerate(data):
        datanp[i, :4] = line
    datanp[:, 4] = datanp[:, 2] + datanp[:, 3]  # Total population (male + female)

    return datanp


def main(input: Path):
    data = load_pyramid_csv(input)
    adist = AliasedDistribution(data[:, 4])
    print(f"Alias table (total population {adist.total:,}):")
    for i, pair in enumerate(zip(adist.probs, adist.alias)):
        print(f"{i:2}: {pair[0]:13,}, {pair[1]:2}")

    print()

    counts = np.zeros(len(data), dtype=np.int64)
    number = 1_000_000
    samples = adist.sample(number)
    np.add.at(counts, samples, 1)

    for i, count in enumerate(counts):
        print(f"{i:2}: {count/number:.6f}")

    return


if __name__ == "__main__":
    parser = ArgumentParser()
    script_dir = Path(__file__).parent.absolute()
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        default=script_dir / "data" / "United States of America-2023.csv",
    )
    args = parser.parse_args()
    main(args.input)
