# -*- coding: utf-8 -*-

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc

from diltools import load_asc_file, BahrData
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit

rc('font', **{'family': 'sans-serif',
              'sans-serif': ['Arial'], 'size': 13})

K = 273.15


def dl_ferrite(TC):
    T = TC + K
    dl0 = 103.9e-4
    B = 18.3e-6
    Th = 320
    return dl0 + B*T + B*Th*(np.exp(-T/Th) - 1)


def dl_austenite(TC):
    T = TC + K
    B = 24.8e-6
    Th = 280
    return B*T + B*Th*(np.exp(-T/Th) - 1)


directory = '/home/arthur/Dropbox/Dilatometria/Arthur_Nishikawa/Cast_Iron/Austempering-15min/isothermal'

files = [
    # ('200.csv', '200 °C'),
    # ('250.csv', '250 °C'),
    ('300.csv', '300 °C'),
    ('375.csv', '375 °C'),
    ('450.csv', '450 °C')
]


fig, ax = plt.subplots(figsize=(6, 4))
for fname, label in files:
    filepath = os.path.join(directory, fname)
    df = pd.read_csv(filepath)
    bd = BahrData(df)
    ax.plot((bd.t - bd.t[0])/60., 100 *
            (bd.dll0 - bd.dll0[0]), lw=1, label=label)

ax.set_xlabel('Tempo (min)')
ax.set_ylabel('Dilatação relativa (%)')
ax.legend(loc='upper left', fancybox=False)
ax.text(.98, .02, 'Austêmpera', ha='right',
        va='bottom', transform=ax.transAxes)

fig.savefig('../dlxt_austempera.svg', bbox_inches='tight')
os.system('svg2pdf ../dlxt_austempera.svg')
plt.show()
plt.close()
