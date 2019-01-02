# -*- coding: utf-8 -*-

import glob

import sys
newdir = '/home/arthur/Dropbox/python'
if newdir not in sys.path:
    sys.path.insert(1, '/home/arthur/Dropbox/python')
from tctools import load_table
from cpartition import FCC, BCC, Interface, WBs, bisect, K

import numpy as np
from scipy.interpolate import interp1d

import matplotlib
matplotlib.rc('font', **{'family':'sans-serif', 'sans-serif':['Arial'], 'size': 13})

def plot_WBs_para(ax):
    directory = '/home/arthur/Dropbox/Thermo-Calc simulations/FoFo_Tupy/TCFE8/'

    para = load_table(directory + 'para_limits.txt', 'T_C')
    tzero = load_table(directory + 't-zero.txt', 'T_C')
    c_exp = [1.66, 1.57, 1.45]
    T_exp = [300, 375, 450]

    T_WBs = []
    caust = []
    for T in [300, 375, 450, 600, 700, 800]:
        try:
            ferr = BCC(T_C=T, tdata=(directory + 'chempot/{}-bcc.txt').format(T), E=WBs(T))
            aust = FCC(T_C=T, tdata=directory + 'chempot/{}-fcc.txt'.format(T))
            intf = Interface(ferr, aust, type_int='equilibrium')
            intf.comp()

            caust.append(aust.x2w(intf.ci_fcc))
            T_WBs.append(T)

            print('  {:} oC; {:.4f} wt.%; {:.1f} J/mol'.format(
                T, 100*caust[-1], float(aust.x2mu['C'](intf.ci_fcc))))
        except Exception as ex:
            print(ex)

    f = interp1d(para['T_C'], 100*para['W(FCC_A1,C)'])
    print('A3 para:', f(T_exp))
    f = interp1d(tzero['T_C'], 100*tzero['W(C)'])
    print('T0:', f(T_exp))

    ax.plot(100*para['W(BCC_A2,C)'], para['T_C'], 'k-', label='A1 para')
    ax.plot(100*para['W(FCC_A1,C)'], para['T_C'], 'k-', label='A3 para')
    ax.plot(100*tzero['W(C)'], tzero['T_C'], 'k--', label='T0')
    ax.plot(100*np.array(caust), T_WBs, 'k-.', label='WBs')
    ax.plot(c_exp, T_exp, 'ks', lw=1, label='Dados experimentais')

    ax.set_xlabel('Teor de carbono (% massa)')
    ax.set_ylabel(u'Temperatura (°C)')
    ax.set_xlim(0, 5.)
    ax.set_ylim(290, 900)

    ax.annotate(s=r'$\gamma$', xy=(3, 700), size=20)
    ax.annotate(s=r'$\alpha + \gamma$', xy=(2.5, 400), size=20)
    ax.annotate(s=r'$A_3^{para}$', xy=(3., 500))
    ax.annotate(s='WBs', xy=(1.4, 500))
    ax.annotate(s=r'$T_0$', xy=(.7, 400))


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(figsize=(6, 4))
    plot_WBs_para(ax)
    fig.savefig('WBs_para.pdf', bbox_inches='tight')
    plt.show()
    # plt.close()
