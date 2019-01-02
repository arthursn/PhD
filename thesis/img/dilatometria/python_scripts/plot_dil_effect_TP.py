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


directory = '/home/arthur/Dropbox/Dilatometria/Arthur_Nishikawa/Cast_Iron/QP-2h'

files = [
    # ('1_fofo_Q&P_PT170-QT200-2h_05.04.15.asc', r'$T_P =$' + '200 °C', 200),
    # ('1_fofo_Q&P_PT170-QT250-2h_05.05.15.asc', r'$T_P =$' + '250 °C', 250),
    ('1_fofo_Q&P_PT170-QT300-2h_05.05.15.asc', r'$T_P =$' + '300 °C', 300),
    ('1_fofo_Q&P_PT170-QT375-2h_05.01.15.asc', r'$T_P =$' + '375 °C', 375),
    ('1_fofo_Q&P_PT170-QT450-2h_05.07.15.asc', r'$T_P =$' + '450 °C', 450)
]

fig, ax = plt.subplots(figsize=(6, 4))
for fname, label, T in files:
    filepath = os.path.join(directory, fname)
    df = load_asc_file(filepath)
    bdlist = BahrData(df, 10e3).split_segments()

    bd = bdlist[-3]
    ax.plot((bd.t - bd.t[0])/60., 100 *
            (bd.dll0 - bd.dll0[0]), lw=1, label=label)

ax.set_xlabel('Tempo de partição (min)')
ax.set_ylabel('Dilatação relativa (%)')
ax.legend(loc='lower right', fancybox=False)
ax.text(.02, .98, r'$T_T =$' + '170 °C', ha='left',
        va='top', transform=ax.transAxes)

fout = '../dlxt_QT=170-PT.svg'
fig.savefig(fout, bbox_inches='tight')
os.system('svg2pdf {}'.format(fout))
plt.show()
plt.close()
