import itertools

import numpy as np
from scipy.stats import qmc


def cartesian_product(*iterables):
    """Return cartesian product of input iterables.

    Uses `itertools.product`

    Parameters
    ----------
    *iterables
        Input iterables.

    Returns
    -------
    list[Any]
        List of product of input arguments.
    """
    return list(itertools.product(*iterables))


def _sampler(func, *iterables, n_samples: int, **kwargs):
    """Generic sampler."""
    bounds = tuple(len(iterable) for iterable in iterables)

    sampler = func(d=len(iterables), **kwargs)
    unit_samples = sampler.random(n_samples)

    indices = np.floor(unit_samples * np.array(bounds)).astype(int)

    samples = []
    for row in indices:
        samples.append(tuple(arg[col] for col, arg in zip(row, iterables)))

    return samples


def latin_hypercube(*iterables, n_samples: int, **kwargs):
    """Sample input iterables using Latin hypercube sampling (LHS).

    Uses `scipy.stats.qmc.LatinHyperCube`.

    Parameters
    ----------
    *iterables
        Iterables to sample from.
    n_samples : int
        Number of samples to return.
    **kwargs
        These keyword arguments are passed to `scipy.stats.qmc.LatinHypercube`

    Returns
    -------
    samples : list[Any]
        List of sampled input arguments.
    """
    return _sampler(qmc.LatinHypercube,
                    *iterables,
                    n_samples=n_samples,
                    **kwargs)


def sobol(*iterables, n_samples: int, **kwargs):
    """Sample input iterables using the Sobol sampling method for generating
    low discrepancy sequences.

    Uses `scipy.stats.qmc.Sobol`.

    Parameters
    ----------
    *iterables
        Iterables to sample from.
    n_samples : int
        Number of samples to return. Note that Sobol sequences lose their
        balance  properties if one uses a sample size that is not a power
        of two.
    **kwargs
        These keyword arguments are passed to `scipy.stats.qmc.Sobol`

    Returns
    -------
    samples : list[Any]
        List of sampled input arguments.
    """
    return _sampler(qmc.Sobol, *iterables, n_samples=n_samples, **kwargs)


def halton(*iterables, n_samples: int, **kwargs):
    """Sample input iterables using the Halton sampling method.

    Uses `scipy.stats.qmc.Halton`.

    Parameters
    ----------
    *iterables
        Iterables to sample from.
    n_samples : int
        Number of samples to return.
    **kwargs
        These keyword arguments are passed to `scipy.stats.qmc.Halton`

    Returns
    -------
    samples : list[Any]
        List of sampled input arguments.
    """
    return _sampler(qmc.Halton, *iterables, n_samples=n_samples, **kwargs)