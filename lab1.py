from crand import crand
from utils import Random, Drawer

generator = Random(0, 10, generator=crand)
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
    ],
    title="Uniform distribution",
)
drawer.draw_distribution(n=500)
