import numpy as np
from scipy.interpolate import griddata


class steam():
    def __init__(self, pressure, T=None, x=None, v=None, h=None, s=None, name=None):
        self.p = pressure
        self.T = T
        self.x = x
        self.v = v
        self.h = h
        self.s = s
        self.name = name
        self.region = None
        if T is None and x is None and v is None and h is None and s is None:
            return
        else:
            self.calc()

    def calc(self):
        data = np.array([
            [0.01, 0.00611657, 0.000611783, 2500.9109946395, 0, 9.1554914737, 0.0010002063, 205.9974594854],
            [4, 0.0081354938, 16.8127172951, 2508.237464527, 0.0611009773, 9.0505562347, 0.0010000743, 157.1213322514],
            # Add the rest of the data here
            [374.14, 220.9, 2099.3, 2099.3, 4.4298, 4.4298, 0.003155, 0.003155]
        ])

        ts = data[:, 0]
        ps = data[:, 1]
        hfs = data[:, 2]
        hgs = data[:, 3]
        sfs = data[:, 4]
        sgs = data[:, 5]
        vfs = data[:, 6]
        vgs = data[:, 7]

        R = 8.314 / (18 / 1000)
        Pbar = self.p / 10  # Convert pressure from bar to kPa

        Tsat = float(griddata((ps), ts, Pbar))
        hf = float(griddata((ps), hfs, Pbar))
        hg = float(griddata((ps), hgs, Pbar))
        sf = float(griddata((ps), sfs, (Pbar)))
        sg = float(griddata((ps), sgs, (Pbar)))
        vf = float(griddata((ps), vfs, (Pbar)))
        vg = float(griddata((ps), vgs, Pbar))

        self.hf = hf

        if self.T is not None:
            if self.T > Tsat:
                self.region = 'Superheated'
                self.h = griddata((ts, ps), hgs, (self.T, Pbar))
                self.s = griddata((ts, ps), sgs, (self.T, Pbar))
                self.x = 1.0
                TK = self.T + 273.14
                self.v = R * TK / (self.p * 1000)
        elif self.x is not None:
            self.region = 'Saturated'
            self.T = Tsat
            self.h = hf + self.x * (hg - hf)
            self.s = sf + self.x * (sg - sf)
            self.v = vf + self.x * (vg - vf)
        elif self.h is not None:
            self.x = (self.h - hf) / (hg - hf)
            if self.x <= 1.0:
                self.region = 'Saturated'
                self.T = Tsat
                self.s = sf + self.x * (sg - sf)
                self.v = vf + self.x * (vg - vf)
            else:
                self.region = 'Superheated'
                self.T = griddata((hgs, ps), ts, (self.h, Pbar))
                self.s = griddata((hgs, ps), sgs, (self.h, Pbar))
        elif self.s is not None:
            self.x = (self.s - sf) / (sg - sf)
            if self.x <= 1.0:
                self.region = 'Saturated'
                self.T = Tsat
                self.h = hf + self.x * (hg - hf)
                self.v = vf + self.x * (vg - vf)
            else:
                self.region = 'Superheated'
                self.T = griddata((sgs, ps), ts, (self.s, Pbar))
                self.h = griddata((sgs, ps), hgs, (self.s, Pbar))

    def print(self):
        print('Name:', self.name)
        if self.x < 0.0:
            print('Region: compressed liquid')
        else:
            print('Region:', self.region)
        print('p = {:0.2f} kPa'.format(self.p))
        if self.x >= 0.0:
            print('T = {:0.2f} degrees C'.format(self.T))
        print('h = {:0.2f} kJ/kg'.format(self.h))
        if self.x >= 0.0:
            print('s = {:0.4f} kJ/(kg K)'.format(self.s))
            if self.region == 'Saturated':
                print('v = {:0.6f} m^3/kg'.format(self.v))
            if self.region == 'Saturated':
                print('x = {:0.4f}'.format(self.x))
        print()


def main():
    inlet = steam(7350, name='Turbine Inlet')
    inlet.x = 0.9
    inlet.calc()
    inlet.print()

    h1 = inlet.h
    s1 = inlet.s
    print(h1, s1, '\n')

    outlet = steam(100, s=inlet.s, name='Turbine Exit')
    outlet.print()

    another = steam(8575, h=2050, name='State 3')
    another.print()
    yetanother = steam(8575, h=3125, name='State 4')
    yetanother.print()


if __name__ == "__main__":
    main()
