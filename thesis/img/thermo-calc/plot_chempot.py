# -*- coding: utf-8 -*-

import glob

import sys
newdir = '/home/arthur/Dropbox/python'
if newdir not in sys.path:
    sys.path.insert(1, '/home/arthur/Dropbox/python')
from tctools import load_table
from cpartition import FCC, BCC, Interface, WBs, bisect, K, x2wp

import numpy as np
from scipy.interpolate import interp1d

import matplotlib
matplotlib.rc('font', **{'family':'sans-serif', 'sans-serif':['Arial'], 'size': 13})

def plot_chempot(ax, Tlist=[300, 375, 450]):
    directory = '/home/arthur/Dropbox/Thermo-Calc simulations/FoFo_Tupy/Fe-C-Mn-Si/'

    df = load_table(directory + 'bcc-cem_ortho.txt', 'T_C')
    mu_ortho = interp1d(df['T_C'], df['MU(C)'])

    df = load_table(directory + 'bcc-cem_para.txt', 'T_C')
    mu_para = interp1d(df['T_C'], df['MU(C)'])

    c_exp = {'300': 1.66, '375': 1.57, '450': 1.45}

    c0 = 3.34414e-02
    fmart = .43

    directory = '/home/arthur/Dropbox/Thermo-Calc simulations/FoFo_Tupy/TCFE8/'

    for T in Tlist:
        try:
            mart = BCC(T_C=T, z=np.array([0, fmart]), c=np.array([c0, c0]),
                       tdata=directory + 'chempot/{}-bcc.txt'.format(T))
            aust = FCC(T_C=T, z=np.array([0, 1-fmart]), c=np.array([c0, c0]),
                       tdata=directory + 'chempot/{}-fcc.txt'.format(T))
            intf = Interface(mart, aust, 'fixed.balance')
            intf.comp(c0)

            f = interp1d(100*aust.x2w(aust.chempot['X(C)']),
                         aust.chempot['MU(C)'])
            g = interp1d(aust.chempot['MU(C)'],
                         100*aust.x2w(aust.chempot['X(C)']))

            line0 = ax.plot(100*aust.x2w(aust.chempot['X(C)']),
                            aust.chempot['MU(C)'], 'k-')

            ax.annotate(s=u'{} °C'.format(T), xy=(3, f(3)), xytext=(-40, 15),
                        textcoords='offset points', ha='right',
                        arrowprops={'arrowstyle': '->', 'relpos': (1, .5)})

            wi_fcc = 100*aust.x2w(intf.ci_fcc)
            line1 = ax.plot(wi_fcc, f(wi_fcc), 'kx', fillstyle='none')

            muo, mup = mu_ortho(T), mu_para(T)
            line2 = ax.plot(g(muo), muo, 'k^', fillstyle='none')
            line3 = ax.plot(g(mup), mup, 'ko', fillstyle='none')
            print(('  {:} oC;'
                   ' CCE: {:.2f}, {:.3f};'
                   ' ortho: {:.2f}, {:.3f};'
                   ' para: {:.2f}, {:.3f}').format(T,
                                                   float(f(wi_fcc)), float(wi_fcc),
                                                   float(muo), float(g(muo)),
                                                   float(mup), float(g(mup))))

            line4 = ax.plot(c_exp[str(T)], f(c_exp[str(T)]), 'ks')
        except Exception as ex:
            print(ex)

    ax.axvline(.76, color='k', ls='--')
    ax.text(.8, -11000, r'$c_0$')

    ax.set_xlabel('Teor de carbono na austenita (% massa)')
    ax.set_ylabel('Potencial químico do carbono (J/mol)')

    ax.set_xlim(0, 4.5)
    ax.set_ylim(-12000, 42000)

    from matplotlib import ticker
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-1, 1))
    ax.yaxis.set_major_formatter(formatter)

    ax.legend((r'$\mu_C^\gamma$',
               r"$\mu_C^{\alpha'}$" + ' ECC',
               r"$\mu_C^{\alpha',\theta}$" + ' ortocementita',
               r"$\mu_C^{\alpha',\theta}$" + ' paracementita',
               r'Dados experimentais'),
              fancybox=False)


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    c0 = 3.34414e-02
    fmart = .43
    T = 375

    directory = '/home/arthur/Dropbox/Thermo-Calc simulations/FoFo_Tupy/TCFE8/'
    ferr = BCC(T_C=T, tdata=directory + 'chempot/{}-bcc.txt'.format(T), E=WBs(T))
    aust = FCC(T_C=T, tdata=directory + 'chempot/{}-fcc.txt'.format(T))
    intf = Interface(ferr, aust, 'equilibrium')
    intf.comp()

    f = interp1d(100*aust.x2w(aust.chempot['X(C)']),
                 aust.chempot['MU(C)'])
    g = interp1d(aust.chempot['MU(C)'],
                 100*aust.x2w(aust.chempot['X(C)']))
    h = interp1d(aust.chempot['X(C)'], aust.chempot['MU(C)'])

    print(h(c0))
    print(h(intf.ci_fcc))

    fig, ax = plt.subplots(figsize=(6, 4))
    plot_chempot(ax=ax)
    fig.savefig('CCE.pdf', bbox_inches='tight')
    plt.show()