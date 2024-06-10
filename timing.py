"""
Compare to numpy's random.Generator.choice method
"""

import matplotlib.pyplot as plt
import numpy as np
import time
import gc

from pyramid_alias import AliasedDistribution

def vose(bins, samples):
    adist = AliasedDistribution(bins)
    return adist.sample(samples)

def numpy(bins, samples):
    rng = np.random.default_rng()
    return rng.choice(len(bins), size=samples, p=bins / bins.sum(), replace=True)

if __name__ == "__main__":

    samples = [100_000, 1_000_000, 10_000_000]
    n_bins = [20, 100, 1000]

    vt = []
    npt = []
    for sample in samples:
        for n in n_bins:
            bins = np.random.randint(1, 100, n).astype(np.int64)

            gc.collect()
            start_time = time.time()
            vose(bins, sample)
            end_time = time.time()
            vt.append(end_time - start_time)

            gc.collect()
            start_time = time.time()
            numpy(bins, sample)
            end_time = time.time()
            npt.append(end_time - start_time)

    vt = np.array(vt).reshape(len(samples), len(n_bins))
    npt = np.array(npt).reshape(len(samples), len(n_bins))

    fig, axes = plt.subplots(1, len(n_bins), figsize=(15, 5), sharey=True)
    for i in range(len(n_bins)):
        ax = axes[i]
        ax.plot(samples, vt.T[i,:],label='Vose')
        ax.plot(samples, npt.T[i,:], label='Numpy')
        ax.set_xscale('log')
        if i == 0:
            ax.legend(frameon=False)
        ax.set_title(f'{n_bins[i]} bins')
    plt.savefig("timing.png")