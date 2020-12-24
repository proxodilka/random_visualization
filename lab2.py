import numpy as np

from utils import Drawer, NormalDistribution


def normal_distribution(low, high, n, scale=3):
    center = (high - low) / 2
    return np.round(np.random.normal(center, scale, size=n)).astype(np.int)


generator = NormalDistribution(0, 20, generator=normal_distribution)
drawer = Drawer(
    generator,
    sliders=[
        {
            "label": "N",
            "valmin": 10,
            "valmax": 50_000,
            "valinit": 500,
            "valstep": 100,
        },
        {"label": "Scale", "valmin": 0.5, "valmax": 6, "valstep": 0.25, "valinit": 3},
    ],
    intervals=5,
    title="Normal distribution",
)
drawer.draw_distribution(n=500, scale=3)
