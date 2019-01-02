# -*- coding: utf-8 -*-

import os
import sys

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib
newdir = '/home/arthur/Dropbox/python'
if newdir not in sys.path:
    sys.path.insert(1, newdir)
from diltools import load_asc_file, BahrData, smooth_derivative

matplotlib.rc('font', **{'family': 'sans-serif',
                         'sans-serif': ['Arial'], 'size': 13})

fname = ('/home/arthur/Dropbox/Dilatometria/Arthur_Nishikawa/'
         'Cast_Iron/QP-2h/1_fofo_Q&P_PT170-QT300-2h_05.05.15.asc')
df = load_asc_file(fname)
bd = BahrData(df, l0=10e3)

fig, ax1 = plt.subplots(figsize=(5, 4))
ax2 = ax1.twinx()

line2, = ax2.plot(bd.t/60, bd.T, 'k--', label='Temperatura')
line1, = ax1.plot(bd.t/60, 100*bd.dll0, 'k-', label='Dilatação')

ax1.set_xlabel(u'Tempo (min)')
ax1.set_ylabel(u'Dilatação relativa (%)')
ax2.set_ylabel(u'Temperatura (°C)')

ax1.legend((line1, line2), ('Dilatação', 'Temperatura'), fancybox=False)

xy, w, h = (30, -.3), 5, .7
# rect = patches.Rectangle(xy, w, h, lw=1, ec='k', ls='--', fc='none')
# ax1.add_patch(rect)

fout = '../170-300.svg'
fig.savefig(fout, bbox_inches='tight')
os.system('svg2pdf {}'.format(fout))

ax1.set_xlim(xy[0], xy[0] + w)
ax1.set_ylim(xy[1], xy[1] + h)
ax2.set_ylim(0, 400)
ax1.axvline(31.696, color='k', ls=':')
ax1.axvline(32.709, color='k', ls=':')
ax1.axvline(32.834, color='k', ls=':')
ax1.text(31.696+.05, -.23, u'Etapa de\ntêmpera')
ax1.annotate('', xy=(31.696, -.25), xytext=(32.709, -.25),
             ha='center', arrowprops=dict(arrowstyle='<->'))
ax1.text(32.834+.05, -.23, u'Etapa de\npartição')
ax1.annotate('', xy=(32.834, -.25), xytext=(33.709, -.25),
             ha='center', arrowprops=dict(arrowstyle='<-'))

ax1.legend((line1, line2), ('Dilatação', 'Temperatura'),
           loc='upper left', fancybox=False)

fout = '../170-300_close.svg'
fig.savefig(fout, bbox_inches='tight')
os.system('svg2pdf {}'.format(fout))

# plt.show()
