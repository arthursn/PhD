# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib
import sys
newdir = '/home/arthur/Dropbox/python'
if newdir not in sys.path:
    sys.path.insert(1, newdir)
from diltools import load_asc_file, BahrData
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit

matplotlib.rc('font', **{'family': 'sans-serif',
                         'sans-serif': ['Arial'], 'size': 13})

directory = '/home/arthur/Dropbox/Dilatometria/Arthur_Nishikawa/Cast_Iron/Martensite_transformation/'

file1 = '1_fofo_quenching_5oCs-1_11.05.15.asc'
file2 = '1_reheating-5oCs-1_11.05.15.asc'

df1 = load_asc_file(directory + file1)

# correct df1

df1 = df1.drop(df1.index[list(range(3852, 3854)) +
                         list(range(3925, 3941))])  # drop weird data

# plt.plot(bd1.dll0, marker='o')
# ax2 = plt.gca().twinx()
# ax2.plot(bd1.T, marker='s')
# plt.show()

bd1 = BahrData(df1, l0=10e3)  # BahrData object file1
p = np.polyfit(bd1.T[3852:3923], bd1.dll0[3852:3923], deg=1)
d1 = np.polyval(p, bd1.T[3851]) - bd1.dll0[3851]
d2 = np.polyval(p, bd1.T[3923]) - bd1.dll0[3923]
bd1.dll0[3852:] = bd1.dll0[3852:] - d1
bd1.dll0[3923:] = bd1.dll0[3923:] + d2

# end snippet

bd2 = BahrData(load_asc_file(directory + file2),
               l0=10e3)  # BahrData object file2
Delta_l = (9.8339-9.8244)/10.

fig, ax = plt.subplots(figsize=(4, 4))

x = np.array([25, 400])

# martensite transformation segment
sel0 = (bd1.T < 880) & (bd1.t > 1800)
x0 = bd1.T[sel0]
y0 = 100.*(bd1.dll0[sel0] - bd1.dll0[sel0][-1])

# austenite linear dilation segment
sel1 = (bd1.T > 250) & (bd1.T < 300) & (bd1.t > 1800)
x1 = bd1.T[sel1]
y1 = 100.*(bd1.dll0[sel1] - bd1.dll0[sel0][-1])
p1 = np.polyfit(x1, y1, deg=1)
fp1 = lambda x: np.polyval(p1, x)

# martensite linear dilation segment
sel2 = (bd2.T < 100) & (bd2.t < 100)
x2 = bd2.T[sel2]
y2 = 100.*(bd2.dll0[sel2] - bd2.dll0[sel2][0] + Delta_l)
p2 = np.polyfit(x2, y2, deg=1)
fp2 = lambda x: np.polyval(p2, x)

each = 1
ax.plot(x0[::each], y0[::each], 'k-', label=u'Têmpera')
ax.plot(x2[::each], y2[::each], 'k--', label=u'Reaquecimento')

ax.legend(loc='upper left', fancybox=False)

xy, w, h = (25, -.5), 375, .75
ax.set_ylim(-.6)
rect = patches.Rectangle(xy, w, h, lw=1, ec='k', ls=':', fc='none')
ax.add_patch(rect)

ax.set_xlabel(u'Temperatura (°C)')
ax.set_ylabel(u'Dilatação relativa (%)')

fig.savefig(u'../dil_martensita.pdf', bbox_inches='tight')

plt.close()

##########

fig, ax = plt.subplots(figsize=(5, 4))

ax.plot(x0[::each], y0[::each], 'k-', label='Dados experimentais')

ax.plot(x, np.polyval(p1, x), 'k:')

ax.plot(x2[::each], y2[::each], 'k--')
ax.plot(x, np.polyval(p2, x), 'k:')

f = (y0 - np.polyval(p1, x0))/(np.polyval(p2, x0) - np.polyval(p1, x0))
g = interp1d(x0, y0)


ax.annotate(r'Ms$\approx$' + u'230 °C', xy=(235, g(230)-.01), xytext=(25, -10),
            ha='left', textcoords='offset points', arrowprops=dict(arrowstyle='->'))

ax.set_xlabel(u'Temperatura (°C)')
ax.set_ylabel(u'Dilatação relativa (%)')

ax.set_xlim(xy[0], xy[0] + w)
ax.set_ylim(xy[1], xy[1] + h)

T = 160
ax.axvline(T, color='k', ls='--')
ax.annotate(r'$T_T$', (T + 5, xy[1] + .02*h))
ax.annotate('', xy=(T, fp1(T)), xytext=(T, g(T)), ha='center', arrowprops=dict(arrowstyle='<->'))
ax.annotate('', xy=(T, fp2(T)), xytext=(T, g(T)), ha='center', arrowprops=dict(arrowstyle='<->'))
ax.annotate('A', (T - 5, .5*(fp1(T) + g(T))), ha='right')
ax.annotate('B', (T - 5, .5*(fp2(T) + g(T))), ha='right')

fig.savefig(u'../dil_martensita_close.pdf', bbox_inches='tight')

plt.show()
# plt.close()
