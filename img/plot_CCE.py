# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data.csv', sep=';')
df.columns = ['TC', 'faustf', 'fausti', 'fmarti', 'fmartfr', 'Caust', 'Cmart']

fig, ax = plt.subplots(figsize=(6,4))
ax2 = ax.twinx()

ax.plot(df.TC, df.Caust, 'k-', label=r"$C^\gamma$")
ax2.plot(df.TC, df.fmarti, 'k--', label=u"Fração inicial de " + r"$\alpha'$")

ax.set_xlabel(u'Temperatura de têmpera (°C)')
ax.set_ylabel(r'$C^\gamma$' + u" (% peso)")
ax2.set_ylabel(u"Fração inicial de " + r"$\alpha'$")

ax.legend(loc='lower left', fancybox=False)
ax2.legend(loc='upper right', fancybox=False)

fig.savefig('CCE_scheme.pdf')

plt.show()



