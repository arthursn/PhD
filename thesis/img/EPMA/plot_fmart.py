# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.axes_grid1 import make_axes_locatable
from itertools import cycle

matplotlib.rc('font', **{'family': 'sans-serif',
                         'sans-serif': ['Arial'], 'size': 13})


def add_label(ax, label, px=.15, py=.1, size=20, **kwargs):
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    x = float(min(xlim) - np.diff(xlim)*px)
    y = float(max(ylim) + np.diff(ylim)*py)
    ax.text(x=x, y=y, s=label, size=size, **kwargs)


def get_alpha(C=0, Mn=0, Si=0, Cr=0, Ni=0, Mo=0):
    alpha = 27.2 - 19.8*(1 - np.exp(-1.56*C)) - \
        (0.14*Mn + 0.21*Si + 0.11*Cr + 0.08*Ni + 0.05*Mo)
    return alpha*1e-3


def get_Ms(C=0, Mn=0, Si=0, Cr=0, Ni=0, Mo=0):
    return 565. - 600.*(1 - np.exp(-0.96*C)) - \
        (31*Mn + 13*Si + 10*Cr + 18*Ni + 12*Mo)
    # return 462 - 273*C - 26*Mn - 16*Ni - 13*Cr - 30*Mo
    # return 539 - 423*C - 30.4*Mn - 17.7*Ni - 12.1*Cr - 7.5*Mo


# def KM(QT, alpha=1.2169e-2, Ms=216.2):
    # return 1 - np.exp(-alpha*(Ms - QT))
def KM(T, alpha=1.2169e-2, Ms=216.2):
    fmart = 1. - np.exp(-alpha*(Ms - T))
    if isinstance(fmart, (np.ndarray)):
        fmart[fmart < 0] = 0
        return fmart
    else:
        return fmart if T < Ms else 0


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
plt.subplots_adjust(wspace=.25)

QT = 170.
vmin, vmax = 0, 70

w = pd.read_csv('EPMA.csv')

comp = dict(C=w['C'].values, Mn=w['Mn'].values, Si=w['Si'].values)
alpha = get_alpha(**comp)
Ms = get_Ms(**comp)
f = 100.*KM(QT, alpha, Ms)

graphite = w['Si'] < 1.
matrix = np.logical_not(graphite)

f[graphite] = 0.

mapcolor = ax1.imshow(f.reshape(400, -1), vmin=vmin,
                      vmax=vmax, extent=(0, 200, 0, 200), cmap=plt.get_cmap('viridis'))
ax1.axes.get_xaxis().set_visible(False)
ax1.axes.get_yaxis().set_visible(False)
add_label(ax1, label='(a)', px=-.45, py=-1.37, size=16)
add_label(ax1, label=r"$f^{\alpha'}$ - " + u'{:.0f} °C'.format(QT), px=-.030, py=-.09,
          size=13, bbox=dict(facecolor='white', edgecolor='None'))

from matplotlib_scalebar.scalebar import ScaleBar
scalebar = ScaleBar(1e-6)
scalebar.location = 'lower right'
ax1.add_artist(scalebar)

divider = make_axes_locatable(ax1)
cax = divider.append_axes('bottom', size='5%', pad=0.1)
cbar = plt.colorbar(mapcolor, cax=cax, orientation='horizontal')
cbar.ax.xaxis.tick_bottom()
cbar.ax.xaxis.set_label_position('bottom')
cbar.ax.set_xlabel(r"$f^{\alpha'}$" + u' (% vol.)')

bins = np.arange(0, 100, 2)
cycolor = cycle([(.12, .47, .71, .7), (1., .5, .05, .7),
                 (.17, .63, .17, .7), (.84, .15, .15, .7)])
for QT in [25, 140, 170, 200]:
    f = 100.*KM(QT, alpha, Ms)

    favg = np.mean(f[matrix])
    favgsd = np.std(f[matrix])
    print(QT, favg, favgsd)
    weights = np.repeat(100., len(f[matrix]))/len(f)
    freq, x, _ = ax2.hist(f[matrix], bins=bins, weights=weights, edgecolor='k',
                          linewidth=.5, facecolor=next(cycolor), label=u'{:.0f} °C'.format(QT))
    ax2.axvline(favg, color='k', ls='--', lw=1)
    ax2.annotate('{:.1f}\n({:.1f})'.format(favg, favgsd), xy=(favg, np.max(freq)),
                 xytext=(-2, 5), ha='right', va='bottom', textcoords='offset points', size=12)

    ax2.set_xlabel(r"$f^{\alpha'}$" + u' (% vol.)')
    ax2.set_ylabel(u'Frequência (%)')

ax2.set_xlim(0, 100)
ax2.set_ylim(0, 50)
ax2.legend(fancybox=False)

add_label(ax2, label='(b)', px=-.45, py=-1.25, size=16)

fig.savefig('EPMA_fmart.pdf', bbox_inches='tight')
