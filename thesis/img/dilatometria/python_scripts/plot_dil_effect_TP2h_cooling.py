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
    bd = BahrData(load_asc_file(filepath), 10e3)

    bdlist = bd.split_segments()
    bdr = bdlist[-4]  # reheating
    bdfc = bdlist[-1]  # final cooling

    ax.plot(bd.T[-3000:], 100*(bd.dll0[-3000:] -
                               bdr.dll0[0]), lw=1, label=label)

    if T == 450:
        sel = bdr.T < 300
        x, y = bdr.T[sel], 100*(bdr.dll0[sel] - bdr.dll0[0])
        p = np.polyfit(x, y, deg=1)
        x = np.linspace(170, 500, 2)
        ax.plot(x, np.polyval(p, x), 'k:', lw=1)

        x, y = bdr.T, 100*(bdr.dll0 - bdr.dll0[0])
        f = interp1d(x, y)

ax.set_xlim(0, 500)
ax.set_ylim(-.3, .9)
ax.set_xlabel('Tempo de partição (min)')
ax.set_ylabel('Dilatação relativa (%)')
ax.legend(loc='upper left', fancybox=False)

xlim = ax.get_xlim()
ylim = ax.get_ylim()
ax.text(.98, .02, r'$T_T =$' + '170 °C', ha='right',
        va='bottom', transform=ax.transAxes)
ax.annotate(s='', xy=(320, f(320)), xytext=(
    320, ylim[0]), arrowprops={'arrowstyle': '<-'})
ax.text(310, ylim[0], '320 °C', ha='right', va='bottom')

fout = '../dlxT_qPT2h_fc.svg'
fig.savefig(fout, bbox_inches='tight')
os.system('svg2pdf {}'.format(fout))
plt.show()
plt.close()
