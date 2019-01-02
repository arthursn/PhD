# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from itertools import cycle
from scipy.interpolate import interp1d

matplotlib.rc('font', **{'family': 'sans-serif',
                         'sans-serif': ['Arial'], 'size': 13})

fig, ax1 = plt.subplots(figsize=(6, 4))
plt.subplots_adjust(hspace=.3)

df_Vieira = pd.read_csv('Viera_tempering_1.csv')
ax1.plot(df_Vieira['Temperature'], df_Vieira['Dilation']/100.,
         color='0.6', lw=1.5, label='Vieira et al.')
f = interp1d(df_Vieira['Temperature'], df_Vieira['Dilation']/100.)

df_FoFo = pd.read_table(('/home/arthur/Dropbox/Dilatometria/Arthur_Nishikawa/'
                         'Cast_Iron/Tempering/FoFo-tempering_12oCs-1.asc'), sep=' ')
ax1.plot(df_FoFo['TC1'], df_FoFo['dl.um']/100.,
         color='0', lw=1.5, label='Cast iron')
g = interp1d(df_FoFo['TC1'], df_FoFo['dl.um']/100.)

ax1.annotate(s=u'Carbonetos de transição', xy=(140, f(140)), xytext=(200, 0),
             textcoords='data', ha='left',
             arrowprops={'arrowstyle': '->', 'relpos': (.05, 1)})
ax1.annotate(s=' ', xy=(140, g(140)), xytext=(200, 0),
             textcoords='data', ha='left',
             arrowprops={'arrowstyle': '->', 'relpos': (0, 1)})

ax1.annotate(s=u'Cementita', xy=(440, f(440)), xytext=(400, .7),
             textcoords='data', ha='right',
             arrowprops={'arrowstyle': '->', 'relpos': (1, .5)})
ax1.annotate(s=' ', xy=(450, g(450)), xytext=(400, .7),
             textcoords='data', ha='right',
             arrowprops={'arrowstyle': '->', 'relpos': (1, 0)})

ax1.set_xlim(0, 600)
ax1.set_ylim(-.05, .8)
ax1.set_xlabel(u'Temperatura (°C)')
ax1.set_ylabel(u'Dilatação relativa (%)')
ax1.legend(fancybox=False)

fig.savefig('../dil_extra.pdf', bbox_inches='tight')

plt.show()
plt.close()
