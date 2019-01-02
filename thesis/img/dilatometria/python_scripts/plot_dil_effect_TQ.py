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


directory = '/home/arthur/Dropbox/Dilatometria/Arthur_Nishikawa/Cast_Iron/QP-15min'

files = [('1_fofo_Q&P_PT140-QT300-15min_05.15.14.asc', r'$T_T =$' + '140 °C'),
         ('1_fofo_Q&P_PT170-QT300-15min_05.02.15.asc', r'$T_T =$' + '170 °C'),
         ('1_fofo_Q&P_PT200-QT300-15min_05.16.14.asc', r'$T_T =$' + '200 °C')]


fig, ax = plt.subplots(figsize=(6, 4))

for fname, label in files:
    filepath = os.path.join(directory, fname)
    df = load_asc_file(filepath)
    bdlist = BahrData(df, 10e3).split_segments()

    bd = bdlist[-3]
    ax.plot((bd.t - bd.t[0])/60., 100*(bd.dll0 - bd.dll0[0]), lw=1, label=label)

df = pd.read_csv(('/home/arthur/Dropbox/Dilatometria/Arthur_Nishikawa/'
                  'Cast_Iron/Austempering-15min/isothermal/300.csv'))
bd = BahrData(df)
ax.plot((bd.t - bd.t[0])/60., 100*(bd.dll0 - bd.dll0[0]), lw=1, label=u'Austêmpera')

ax.set_xlabel('Tempo de partição/austêmpera (min)')
ax.set_ylabel('Dilatação relativa (%)')
ax.text(.98, .02, r'$T_P =$' + '300 °C', ha='right', va='bottom', transform=ax.transAxes)
ax.legend(loc='upper left', fancybox=False)

fig.savefig('../dlxt_PT300.svg', bbox_inches='tight')
os.system('svg2pdf ../dlxt_PT300.svg')
plt.show()
plt.close()
