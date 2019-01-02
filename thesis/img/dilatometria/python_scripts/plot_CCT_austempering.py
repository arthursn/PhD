# -*- coding: utf-8 -*-

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc

from tctools import *
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

files = [('200.csv', '200 °C', 200),
         ('250.csv', '250 °C', 250),
         ('300.csv', '300 °C', 300),
         ('375.csv', '375 °C', 375),
         ('450.csv', '450 °C', 450)]

fgraph = .103
fi = .05
ff = .3

pear = load_table('V_BCC_CEM.TXT', 'T')
ferr = load_table('V_BCC.TXT', 'T')
aust = load_table('V_FCC.TXT', 'T')

vpear = interp1d(pear['T'] - K, pear['V'])
vferr = interp1d(ferr['T'] - K, ferr['V'])
vaust = interp1d(aust['T'] - K, aust['V'])

def dlexp(T):
    dl = (vpear(T) - vaust(T))/vpear(25)
    return (1 - fgraph)*dl/3

fig, ax = plt.subplots(figsize=(6, 4))
for fname, label, T in files:
    filepath = os.path.join(directory, fname)
    df = pd.read_csv(filepath)
    bd = BahrData(df)
    t = bd.t - bd.t[0]

    f = (bd.dll0 - bd.dll0[0])/dlexp(T)

    g = interp1d(f, t)

    ax.plot(t, f)
#     ax.plot(g(fi), T, 'kx')
#     try:
#         ax.plot(g(ff), T, 'rx')
#     except:
#         pass

# ax.set_xscale('log')
# ax.set_xlim(1, 1e3)

plt.show()
# plt.close('all')
