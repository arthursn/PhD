# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from cpartition import w2x, K


def D_bcc(T, C=0):
    D0 = 0.02e8*np.exp(-10115./T)   # Pre-exponential term
    # D in um^2/s
    D = D0*np.exp(0.5898*(1. + 2.*np.arctan(1.4985 - 15309./T)/np.pi))
    if isinstance(C, np.ndarray):
        D = np.full(C.shape, D)
    return D


def D_fcc(T, C=0):
    yC = C/(1. - C)
    D0 = 4.53e5*(1. + yC*(1.-yC)*8339.9/T)  # Pre-exponential term
    D = D0*np.exp(-(1./T - 2.221e-4)*(17767 - yC*26436))  # um^2/s
    return D


if __name__ == '__main__':
    y = dict(Cu=3.55354266E-3, Mn=2.05516602E-3,
             Si=5.02504411E-2, Fe=9.4414085022e-1)

    w = np.linspace(0, 6e-2, 100)
    x = w2x(w, y=y)
    T = 375 + K

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(100*w, D_bcc(T, x), 'k--', lw=1,
            label=r'$D_C^\alpha$, ferrita ou martensita')
    ax.plot(100*w, D_fcc(T, x), 'k-', lw=1, label=r'$D_C^\gamma$, austenita')
    ax.text(.02, .98, u'T = 375 °C', size=16,
            ha='left', va='top', transform=ax.transAxes)

    ax.set_yscale('log')
    ax.set_xlabel(u'Teor de carbono (% massa)')
    ax.set_ylabel(r'Difusividade ($\mu m^2/s$)')

    ax.legend(loc='lower right', fancybox=False)

    fig.savefig('difusividades_carbono.svg', bbox_inches='tight')
    import os
    os.system(
        'rsvg-convert -f pdf -o difusividades_carbono.pdf difusividades_carbono.svg')
    plt.show()
    # plt.close()
