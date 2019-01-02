# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from tctools import *

matplotlib.rc('font', **{'family': 'sans-serif',
                         'sans-serif': ['Arial'], 'size': 13})

df = load_table('SOLIDIFICATION_COMP.TXT', 'T')

fig, ax = plt.subplots(figsize=(6,4))

K = 273.15
ax.plot(df['T'] - K, 100*df['W(FCC_A1,SI)'], lw=1, label='Si')
ax.plot(df['T'] - K, 100*df['W(FCC_A1,MN)'], lw=1, label='Mn')
ax.plot(df['T'] - K, 100*df['W(FCC_A1,CU)'], lw=1, label='Cu')
ax.plot(df['T'] - K, 100*df['W(FCC_A1,C)'], lw=1, label='C')

Tl = 1167.60
Te = 1159.02
ax.axvline(Tl, color='k', lw=1, ls='--')
ax.axvline(Te, color='k', lw=1, ls='--')
ax.annotate('', xy=(Tl, 1.), xytext=(Tl-2, 1.), ha='center', arrowprops=dict(arrowstyle='<-'))
ax.annotate('', xy=(Te, 1.), xytext=(Te-2, 1.), ha='center', arrowprops=dict(arrowstyle='<-'))
ax.text(Tl - .1, 1.1, u'Solificação\nprimária', ha='right', va='bottom')
ax.text(Te - .1, 1.1, u'Solificação\neutética', ha='right', va='bottom')

ax.set_xlabel('Temperatura (°C)')
ax.set_ylabel('Composição na austenita (% massa)')
ax.legend(loc='upper right', fancybox=False)

fig.savefig('scheil_austenita.pdf', bbox_inches='tight')
plt.close('all')