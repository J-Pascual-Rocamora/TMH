import math
import numpy as np

READINGS = np.array([
    311.81,
    688.03,
    818.28,
    870.33,
    885.29,
    872.51,
    837.92,
    34.46,
    15.01,
])

TIMES = np.array([
    7*3600+55*60,
    8*3600+55*60,
    9*3600+55*60,
    10*3600+55*60,
    11*3600+55*60,
    12*3600+55*60,
    13*3600+55*60,
    14*3600+55*60,
    15*3600+55*60,
])

class PowerSimulator(object):

    def __init__(self, cell_max_power=3.25):
        self._const = None
        self._cell_max_power = cell_max_power
        self._fit_curve()

    def __repr__(self):
        return '<PowerSimulator: {}>'.format(self._cell_max_power)

    def get_power(self, x):
        # gets the cell power
        # This is separated from the model, in case noise is added
        return self.calculate_power(x)

    def _fit_curve(self):
        # Calculates the polynomial parameters for the fitted curve
        reduction_factor = max(READINGS)/self._cell_max_power
        x_values = [x/reduction_factor for x in READINGS]
        self._const = np.polyfit(TIMES, x_values, 3)
        return

    def calculate_power(self, x):
        # Calculates the cell power for a time x of the day based on the fitted polynomial
        if x < 5.5*3600:
            return 0
        elif x < 7*3600+15*60:
            return (x-5.5*3600) * (0.245846065896488)/(105*60)
        elif x > 15*3600+40*60:
            return (17*3600-x) * 0.09924047440601624/(80*60)
        elif x > 17*3600:
            return 0
        value = 0
        for index, c in enumerate(self._const):
            value += c * (x ** index)
        return value