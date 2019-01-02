# -*- coding: utf-8 -*-

import os

import numpy as np
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


directory = '/home/arthur/Dropbox/Dilatometria/Arthur_Nishikawa/Cast_Iron/QP-5min'

files = [
    ('1_fofo_Q&P_PT170-QT300-5min_05.12.15.asc', r'$T_P =$' + '300 °C', 300),
    ('1_fofo_Q&P_PT170-QT375-5min_05.12.15.asc', r'$T_P =$' + '375 °C', 375),
    ('001_fofo_Q&P_PT170-QT450-5min_04.24.18.asc', r'$T_P =$' + '450 °C', 450)
]

fig, ax = plt.subplots(figsize=(6, 4))
for fname, label, T in files:
    filepath = os.path.join(directory, fname)
    bd = BahrData(load_asc_file(filepath), 10e3)

    bdlist = bd.split_segments()
    bdr = bdlist[-4]  # reheating
    bdfc = bdlist[-1]  # final cooling

    ax.plot(bd.T[-3000:], 100*(bd.dll0[-3000:] -
                               bdr.dll0[0]), lw=1, label=label)

ax.set_xlim(0, 500)
ax.set_ylim(-.3, .9)
ax.set_xlabel('Temperatura de partição (°C)')
ax.set_ylabel('Dilatação relativa (%)')
ax.legend(loc='upper left', fancybox=False)

xlim = ax.get_xlim()
ylim = ax.get_ylim()
ax.text(.98, .02, r'$T_T =$' + '170 °C', ha='right',
        va='bottom', transform=ax.transAxes)

fout = '../dlxT_qPT30s-fc.svg'
fig.savefig(fout, bbox_inches='tight')
os.system('svg2pdf {}'.format(fout))
plt.show()
plt.close()
