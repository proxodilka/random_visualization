from .crandom import crand as _crand

RAND_MAX = 32768


def crand(low=None, high=None, n=1):
    if low is None and high is None:
        low, high = 0, RAND_MAX
    if low is not None and high is None:
        low, high = 0, low
    if low is None:
        low = 0

    return [_crand(low, high) for _ in range(n)]
