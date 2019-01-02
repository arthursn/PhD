# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib
import sys
newdir = '/home/arthur/Dropbox/python'
if newdir not in sys.path:
    sys.path.insert(1, newdir)
from diltools import load_asc_file, BahrData, smooth_derivative

matplotlib.rc('font', **{'family':'sans-serif', 'sans-serif':['Arial'], 'size': 13})

directory = '/home/arthur/Dropbox/Dilatometria/Arthur_Nishikawa/Cast_Iron/Martensite_transformation/'

fname = '../data/1_fofoTupy_10oCmin-1_10.28.14.asc'
df = load_asc_file(fname)
bd = BahrData(df, l0=10e3)

x, y = bd.T[:4400:10], 100*bd.dll0[:4400:10]

fig, ax = plt.subplots(figsize=(4, 4))
ax.plot(x, y, 'k-')
ax.set_xlabel(u'Temperatura (°C)')
ax.set_ylabel(u'Dilatação relativa (%)')

xy, w, h = (600, .8), 280, .72
rect = patches.Rectangle(xy, w, h, lw=1, ec='k', ls=':', fc='none')
ax.add_patch(rect)

fig.savefig('../1_fofoTupy_10oCmin_2.pdf', bbox_inches='tight')

fig, ax = plt.subplots(figsize=(5, 4))
ax2 = ax.twinx()

ax.plot(x, y, 'k-')
ax.set_xlim(xy[0], xy[0] + w)
ax.set_ylim(xy[1], xy[1] + h)
ax.set_xlabel(u'Temperatura (°C)')
ax.set_ylabel(u'Dilatação relativa (%)')

def vertical_line(ax, T):
    ax.axvline(T, color='k', ls=':')
    ax.annotate(u'{:d} °C'.format(int(T)), (T - 5, xy[1] + h*.02), ha='right')

vertical_line(ax, 737)
ax.annotate('A', (.5*(737 + xy[0]), xy[1] + .92*h), ha='center')
vertical_line(ax, 783)
ax.annotate('B', (.5*(783 + 737), xy[1] + .92*h), ha='center')
vertical_line(ax, 854)
ax.annotate('C', (.5*(854 + 783), xy[1] + .92*h), ha='center')
ax.annotate('D', (.5*(854 + 880), xy[1] + .92*h), ha='center')

xx, yy = smooth_derivative(x, y, 5)
ax2.plot(xx, yy, 'k--')
ax2.set_ylim(-.002, .006)
ax2.set_ylabel(u'Derivada (%/°C)')

fig.savefig('../1_fofoTupy_10oCmin.pdf', bbox_inches='tight')

# plt.show()
plt.close('all')