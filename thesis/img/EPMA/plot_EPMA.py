# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.axes_grid1 import make_axes_locatable

matplotlib.rc('font', **{'family': 'sans-serif',
                         'sans-serif': ['Arial'], 'size': 13})

def add_label(ax, label, px=.15, py=.1, size=20, **kwargs):
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    x = float(min(xlim) - np.diff(xlim)*px)
    y = float(max(ylim) + np.diff(ylim)*py)
    ax.text(x=x, y=y, s=label, size=size, **kwargs)

comp = pd.read_csv('EPMA.csv')

avg = {'Si': 2.47, 'Cu': 0.38, 'Mn': 0.20}
label = ['(a)', '(b)', '(c)']
cmap = plt.get_cmap('viridis')

fig, axes = plt.subplots(2, 2, figsize=(8, 8))
axes = axes.reshape(-1, 1)
plt.subplots_adjust(wspace=.25, hspace=.35)

I = {}
i = 0
extent = (0, 200, 0, 200)

for el in ['Si', 'Cu', 'Mn']:
    ax = axes[i][0]

    I[el] = comp[el].values.reshape(400, -1)

    vmin, vmax = avg[el]-2*np.std(I[el]), avg[el]+2*np.std(I[el])
    mapColor = ax.imshow(I[el], vmin=vmin, vmax=vmax, extent=extent, cmap=cmap)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)

    add_label(ax, label=label[i], px=-.45, py=-1.37, size=14)
    add_label(ax, label=u'{}'.format(el), px=-.030, py=-.080,
          size=13, bbox=dict(facecolor='white', edgecolor='None'))

    divider = make_axes_locatable(ax)
    cax = divider.append_axes('bottom', size='5%', pad=0.1)
    cbar = plt.colorbar(mapColor, cax=cax, orientation='horizontal')
    xpos = np.linspace(vmin, vmax, 7)
    xpos = np.around(xpos, decimals=1)
    cbar.set_ticks(xpos)
    cbar.ax.xaxis.tick_bottom()
    cbar.ax.xaxis.set_label_position('bottom')
    cbar.ax.set_xlabel('Composição de {} (% massa)'.format(el))
    # ax.text(s=el, x=15, y=170, backgroundcolor='white')

    ax.axhline(135, color='black', ls='--', lw=1.5)

    if i == 0:
        from matplotlib_scalebar.scalebar import ScaleBar
        scalebar = ScaleBar(1e-6)
        scalebar.location = 'lower right'
        ax.add_artist(scalebar)

    i += 1

I['C'] = comp['C'].values.reshape(400, -1)

ax = axes[i][0]
Si = np.mean(I['Si'][129:131, :], axis=0)
Mn = np.mean(I['Mn'][129:131, :], axis=0)
Cu = np.mean(I['Cu'][129:131, :], axis=0)
C = np.mean(I['C'][129:131, :], axis=0)
C[100:110] = 100.

x = np.linspace(0, 400., 400)
ax.plot(x, Si, lw=1.)
ax.annotate('Si', xy=(x[300], Si[300]), xytext=(0, 25),
            ha='center', textcoords='offset points')
ax.plot(x, Mn, lw=1.)
ax.annotate('Mn', xy=(x[340], Mn[340]), xytext=(
    0, 40), ha='center', textcoords='offset points', arrowprops=dict(arrowstyle='->'))
ax.plot(x, Cu, lw=1.)
ax.annotate('Cu', xy=(x[280], Cu[280]), xytext=(
    0, 40), ha='center', textcoords='offset points', arrowprops=dict(arrowstyle='->'))
ax.plot(x, C, lw=1.)
ax.annotate('C (calc.)', xy=(x[200], C[200]), xytext=(
    0, 10), ha='center', textcoords='offset points')

ax.set_xlabel(u'Posição (μm)')
ax.set_ylabel(r'Composição (% massa)')
ax.set_xlim(x.min(), x.max())
ax.set_ylim(0, 4.)
# ax.set_aspect('equal')
add_label(ax, label='(d)', px=-.45, py=-1.25, size=14)

i += 1


fig.savefig('EPMA.pdf', bbox_inches='tight', dpi=300)
plt.close('all')

