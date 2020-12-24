import numpy as np
from collections import OrderedDict


class Random:
    def __init__(self, low=None, high=None, generator=None, seed=42):
        if low is None and high is None and generator is None:
            raise TypeError(
                "Can't create and instance of `Random`:\n"
                + "You should specify either `generator` or range of values."
            )
        if low is not None and high is None:
            low, high = 0, low
        self.low = low
        self.high = high
        self._args = [o for o in [low, high] if o is not None]
        self.seed = seed
        self.generator = (
            generator
            if generator is not None
            else (lambda *args, size: np.random.randint(*args, size=size))
        )
        self._generated = []

    def get_distribution(self, n=None, normalize=True, **kwargs):
        n = int(n)
        if n is None:
            n = len(self._generated)
        arr = self.generate(n=n, **kwargs)
        unique, counts = np.unique(arr, return_counts=True)
        if normalize:
            counts = np.divide(counts, np.sum(counts))
        res = {k: 0 for k in range(self.low, self.high)}
        res.update(dict(zip(unique, counts)))
        return OrderedDict(sorted(res.items()))

    def get_distribution_intervals(self, distribution, normalize=True, intervals=5):
        counts = np.array(
            [
                np.sum(
                    [distribution.get(i, 0) for i in range(int(k), int(k + intervals))]
                )
                for k in distribution.keys()
            ]
        )
        if normalize:
            counts = np.divide(counts, np.sum(counts))
        return OrderedDict({k: v for k, v in zip(distribution.keys(), counts)})

    def generate(self, n, force=False, **kwargs):
        if force:
            self._generated = []
        if n <= len(self._generated):
            return self._generated[:n]
        to_generate = n - len(self._generated)
        new_sequence = self.generator(*self._args, n=to_generate, **kwargs)
        self._generated = np.concatenate([self._generated, new_sequence])
        return self._generated


class NormalDistribution(Random):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale = 3

    def generate(self, n, force=False, scale=3, **kwargs):
        if scale != self.scale:
            self.scale = scale
            force = True
        return super().generate(n=n, force=force, scale=scale, **kwargs)
