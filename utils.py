import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

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


class Drawer:
    SLIDERS_COORDS = [0.25, None, 0.5, 0.03]
    SLIDERS_HEIGHT = 0.03
    SLIDERS_MARGIN = 0.02

    BASE_PLOT_MARGIN = 0.18
    PLOT_MARGIN = 0.05

    def __init__(self, generator, sliders=None, title="Random distribution"):
        self.generator = generator
        self.figure, axes = plt.subplots()
        self.figure.set_size_inches(8, 6)
        self.is_active = False

        nsliders = len(sliders) if sliders else 0

        if nsliders:
            plot_bottom_margin = self.BASE_PLOT_MARGIN + self.PLOT_MARGIN * (
                nsliders - 1
            )
            self.figure.subplots_adjust(bottom=plot_bottom_margin)

        self.axes = axes
        self.axes.set_xlim(self.generator.low, self.generator.high - 1)
        self.axes.set_xlabel("Random value")
        self.axes.set_ylabel("Probability")
        self.axes.set_title(title)

        self.sliders = []

        if sliders:
            for i, slider in enumerate(sliders):
                self.add_slider(slider, i)

    def draw_distribution(self, **kwargs):
        distribution = self.generator.get_distribution(**kwargs)
        x, y = list(distribution.keys()), list(distribution.values())
        max_value = np.max(y)
        y_lim = min(1, max_value * 2)

        self.axes.set_ylim(0, y_lim)
        if not self.is_active:
            self.bar = self.axes.bar(x, y, color="blue")
            self.plot = self.axes.plot(x, y, color="red", linewidth=2, linestyle="--")[
                0
            ]
            self.is_active = True
            plt.show()
        else:
            self.plot.set_xdata(x)
            self.plot.set_ydata(y)
            self.bar.remove()
            self.bar = self.axes.bar(x, y, color="blue")
            self.figure.canvas.draw_idle()

    def add_slider(self, slider, n):
        ax = self.figure.add_axes(self.get_slider_coords(n + 1))
        slider = Slider(ax, **slider)
        slider.on_changed(lambda value: self.execute_callback())
        self.sliders.append(slider)

    def execute_callback(self):
        kwargs = {
            slider.label.get_text().lower(): slider.val for slider in self.sliders
        }
        self.draw_distribution(**kwargs)

    @classmethod
    def get_slider_coords(cls, n):
        result = cls.SLIDERS_COORDS
        result[1] = cls.SLIDERS_HEIGHT * n + cls.SLIDERS_MARGIN * (n - 1)
        return tuple(result)
