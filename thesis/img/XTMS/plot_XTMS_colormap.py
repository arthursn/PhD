import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.axes_grid1 import make_axes_locatable
from itertools import cycle

matplotlib.rc('font', **{'family': 'sans-serif',
                         'sans-serif': ['Arial'], 'size': 13})


def d_spacing(tth, lmb=1.0332):
    return(.5*lmb/np.sin(np.pi*tth/360))


def parse_peakname(peakname):
    ph = peakname[0]
    hkl = '(' + peakname[1:] + ')'
    if ph == 'f':
        ph = r'$\alpha$'
    elif ph == 'a':
        ph = r'$\gamma$'
    return hkl + ph


# loading files
try:
    data_mythen
except:
    filepath = '/home/arthur/Documents/XTMS/2015-05/Resultados_FoFo/QP/raw_Mythen/FoFo_PT300-2h.mythen'
    data_mythen = pd.read_table(filepath, sep=' ', comment='#',
                                header=None, names=['tth', 'num', 'mythen'])

try:
    peaks
except:
    filepath = '/home/arthur/Documents/XTMS/2015-05/Resultados_FoFo/QP/tth/FoFo_PT300-2h_tth.dat'
    peaks = pd.read_table(filepath, sep=' ')

xmin, xmax = 150, 400
tth = data_mythen['tth'].values
I = data_mythen['mythen'].values

Im = I.reshape(-1, 2560)
tthm = tth.reshape(-1, 2560)
dm = d_spacing(tthm)

time = np.linspace(0, 120, Im.shape[0])
timem = np.repeat(time, Im.shape[1]).reshape(Im.shape[0], -1)

# plotting

fig, ax = plt.subplots(figsize=(7, 5))
mapcolor = ax.pcolormesh(tthm, timem, np.log(Im), vmin=3)
# https://matplotlib.org/examples/misc/rasterization_demo.html
mapcolor.set_rasterized(True)

divider = make_axes_locatable(ax)
cax = divider.append_axes('right', size='5%', pad=0.1)
cbar = plt.colorbar(mapcolor, cax=cax, orientation='vertical')
cax.set_ylabel('log(Intensidade)')

for col in peaks.columns:
    if col != 'index' and col != 'time':
        peakname = parse_peakname(col)
        x, ytxt = peaks[col].values[-1], 124
        xtxt = x
        if col == 'a111':
            xtxt -= .7
        if col == 'f110':
            xtxt += .7
        ax.annotate(s=peakname, xy=(x, 120),
                    xytext=(xtxt, ytxt), ha='center')

ax.set_xlabel(r'2$\theta$ ' + u'(°)')
ax.set_ylabel(u'Tempo de partição (min)')

fig.savefig('XTMS_colormap_full.pdf', bbox_inches='tight')

plt.close(fig)

###########

fig, ax = plt.subplots(figsize=(6, 5))
mapcolor = ax.pcolormesh(dm, timem, np.log(Im), vmin=3)
# https://matplotlib.org/examples/misc/rasterization_demo.html
mapcolor.set_rasterized(True)

divider = make_axes_locatable(ax)
cax = divider.append_axes('right', size='5%', pad=0.1)
cbar = plt.colorbar(mapcolor, cax=cax, orientation='vertical')
cax.set_ylabel('log(Intensidade)')

ax.set_xlabel(u'Distância interplanar ' + r'($\AA$)')
ax.set_ylabel(u'Tempo de partição (min)')

ax.set_xlim(2, 2.14)

a111 = d_spacing(peaks['a111'].values)
f110 = d_spacing(peaks['f110'].values)

ax.plot(a111, peaks['time'].values/60, 'k-')
ax.plot(f110, peaks['time'].values/60, 'k-')

ax.annotate(s=r'(111)$\gamma$', xy=(a111[-1], 120),
            xytext=(a111[-1], 124), ha='center')
ax.annotate(s=r'(110)$\alpha$', xy=(f110[-1], 120),
            xytext=(f110[-1], 124), ha='center')

# fig.tight_layout()
fig.savefig('XTMS_colormap_detail.pdf', bbox_inches='tight')
# plt.show()
plt.close(fig)
