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

x = np.array([25, 400])

# martensite transformation segment
sel0 = (bd1.T < 800) & (bd1.t > 1800)
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

# transformed fraction
f = (y0 - np.polyval(p1, x0))/(np.polyval(p2, x0) - np.polyval(p1, x0))
g = interp1d(x0, y0)

# KM fitting
def KM(T, *args):
    beta, Ms = args
    return 1 - np.exp(beta*(Ms - T))

sel3 = x0 < 200
popt, pcov = curve_fit(KM, x0[sel3], f[sel3], p0=(-.011, 210))
print(popt)

x3 = np.linspace(0, popt[1], 1000)
y3 = KM(x3, *popt)

##########

fig, ax = plt.subplots(figsize=(5, 4))

each = 5


ax.plot(x0[::each], f[::each], 'k-', label='Dados experimentais')
ax.plot(x3, y3, 'k--', label='Curva ajustada')

ax.annotate(r'Ms$\approx$' + u'230 °C', xy=(235, g(230)-.01), xytext=(25, -10),
            ha='left', textcoords='offset points', arrowprops=dict(arrowstyle='->'))
ax.annotate(r'Ms\'$\approx$' + u'216 °C', xy=(216, g(230)-.01), xytext=(25, -10),
            ha='left', textcoords='offset points', arrowprops=dict(arrowstyle='->'))

ax.set_xlim(0, 250)
ax.set_ylim(0, 1)
ax2 = ax.twinx()
ax2.set_ylim(1, 0)
ax.set_xlabel(u'Temperatura (°C)')
ax.set_ylabel(u'Fração de martensita ' + r"($f^{\alpha'}$)")
ax2.set_ylabel(u'Fração de austenita ' + r"($f^{\gamma}$)")

ax.legend(loc='lower left')

fig.savefig(u'../frac_martensita.pdf', bbox_inches='tight')

plt.show()
# plt.close()
