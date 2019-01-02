# -*- coding: utf-8 -*-

import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.interpolate import interp1d

rcParams.update({'font.family': 'sans-serif',
                 'font.sans-serif': 'Arial',
                 'font.size': 13})

colors = rcParams['axes.prop_cycle'].by_key()['color']


def plotXRD(files, ax=None, gap=0, labels=None, colors=None,
            labelannotate=False, fx=lambda x: x, fy=lambda x: x, **kwargs):
    kw = dict()

    if ax is None:
        fig, ax = plt.subplots()

    if labels is None:
        labels = [None]*len(files)

    if colors is None:
        colors = [None]*len(files)

    iterate = list(zip(files, labels, colors))
    n = len(iterate)

    for i, (file, label, color) in enumerate(iterate):
        data = np.loadtxt(file)

        tth = data[:, 0]
        x = fx(tth)

        I = data[:, 2]
        I = fy(I) + i*gap

        if labelannotate:
            xlim = ax.get_xlim()
            ax.annotate(s=label, xy=(xlim[-1], i*gap),
                        xytext=(5, 0), textcoords='offset points')
        elif label:
            kw['label'] = label

        if color:
            kw['color'] = color

        kw['zorder'] = n - i

        kw.update(kwargs)

        ax.plot(x, I, **kw)

    ax.set_xlabel(r'Bragg angle 2$\theta$ ' + u'(°)')
    ax.set_ylabel('Normalized intensities')

    return ax


def plot_indexed_peaks(file2ti, ax, Irng=[.02, .3], fx=lambda x: x, **kwargs):
    data = np.loadtxt(file2ti)

    tth = data[:, 0]
    I = data[:, 1]

    x = fx(tth)

    ylim = ax.get_ylim()

    I = I/I.max()

    ymin = ylim[0] + Irng[0]*(ylim[1] - ylim[0])
    ymax = ymin + I*(Irng[1] - Irng[0])*(ylim[1] - ylim[0])

    ax.vlines(x, ymin, ymax, **kwargs)


if __name__ == '__main__':
    files = [
        'normalized/FoFo-quenched-exsitu-scan_01.txt',
        'normalized/FoFo-QP_PT300_exsitu-scan_01.txt',
        'normalized/FoFo-QP_PT375_exsitu-scan_01.txt',
        'normalized/FoFo-QP_PT450_exsitu-scan_01.txt',
        'normalized/FoFo-tempering_700oC_exsitu-scan_01.txt'
    ]

    labels = [
        'Temperada',
        u'300 °C / 2h',
        u'375 °C / 2h',
        u'450 °C / 2h',
        u'Revenida a 700 °C'
    ]

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.set_xlim(22, 50)

    plotXRD(files=files[:-1], ax=ax, labels=labels[:-1],
            labelannotate=True, gap=8e-2, lw=1)

    ax.set_ylim(-.1)

    ax.set_xlabel(r'$2\theta$ ' + u'(°)')
    ax.set_ylabel('Intensidade normalizada')

    plot_indexed_peaks('ferrite.2ti', ax, label='Ferrita',
                       lw=1.2, color='k')
    plot_indexed_peaks('austenite_a3.65.2ti', ax,
                       label='Austenita ' + r'$a = 3,65 \AA$',
                       lw=1.2, color='r')

    ax.legend(loc=9, bbox_to_anchor=(0.5, -0.12), ncol=2, fancybox=False)

    fig.savefig('selected_diffractograms.pdf', bbox_inches='tight')

    #######

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.set_xlim(22, 50)

    plotXRD(files=files, ax=ax, labels=labels, labelannotate=True,
            gap=5e-4, lw=1)

    ax.set_ylim(-10e-4, 5e-3)

    ax.set_xlabel(r'$2\theta$ ' + u'(°)')
    ax.set_ylabel('Intensidade normalizada')

    plot_indexed_peaks('graphite.2ti', ax, label='Grafita',
                       lw=1.2, color='k')
    plot_indexed_peaks('eta_Hirotsu.2ti', ax, label=r'Carboneto $\eta$',
                       lw=1.2, color='r')
    plot_indexed_peaks('cementite_Wood.2ti', ax, label='Cementita',
                       lw=1.2, color='g')

    i, gap = 4, 5e-4
    data = np.loadtxt(files[i])
    tth, I = data[:, 0], data[:, 2]
    f = interp1d(tth, I + i*gap + gap*.5)
    tthsel = np.array([23.494, 37.1742, 40.6148])
    ax.plot(tthsel, f(tthsel), 'kv', fillstyle='none')

    ax.legend(loc=9, bbox_to_anchor=(0.5, -0.12), ncol=3, fancybox=False)

    fig.savefig('selected_diffractograms_detail.pdf', bbox_inches='tight')

    #######

    files = [
        'normalized/FoFo-QP_PT450_exsitu-scan_01.txt',
        'normalized/FoFo-tempering_700oC_exsitu-scan_01.txt'
    ]

    labels = [
        u'450 °C / 2h',
        u'Revenida a 700 °C'
    ]

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.set_xlim(22, 50)

    plotXRD(files=files, ax=ax, labels=labels, labelannotate=True,
            gap=5e-4, lw=1, colors=colors[3:5])
    
    ax.set_ylim(-10e-4, 3e-3)

    ax.set_xlabel(r'$2\theta$ ' + u'(°)')
    ax.set_ylabel('Intensidade normalizada')

    plot_indexed_peaks('graphite.2ti', ax, label='Grafita',
                       lw=1.2, color='k')
    plot_indexed_peaks('fe3o4.2ti', ax, label=r'$Fe_3O_4$',
                       lw=1.2, color='b')
    plot_indexed_peaks('cementite_Wood.2ti', ax, label='Cementita',
                       lw=1.2, color='g')

    i, gap = 1, 5e-4
    data = np.loadtxt(files[i])
    tth, I = data[:, 0], data[:, 2]
    f = interp1d(tth, I + i*gap + gap*.5)
    tthsel = np.array([23.494, 37.1742, 40.6148])
    ax.plot(tthsel, f(tthsel), 'kv', fillstyle='none')

    ax.legend(loc=9, bbox_to_anchor=(0.5, -0.12), ncol=3, fancybox=False)

    fig.savefig('selected_diffractograms_cementite.pdf', bbox_inches='tight')

    #######

    files = [
        'normalized/FoFo-QP_PT300_exsitu-scan_01.txt',
        'normalized/FoFo-QP_PT375_exsitu-scan_01.txt',
    ]

    labels = [
        u'300 °C / 2h',
        u'375 °C / 2h',
    ]

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.set_xlim(22, 50)
    
    plotXRD(files=files, ax=ax, labels=labels, labelannotate=True,
            gap=5e-4, lw=1, colors=colors[1:3])

    ax.set_ylim(-10e-4, 3e-3)

    ax.set_xlabel(r'$2\theta$ ' + u'(°)')
    ax.set_ylabel('Intensidade normalizada')

    plot_indexed_peaks('graphite.2ti', ax,
                       label='Grafita', lw=1.2, color='k')
    plot_indexed_peaks('epsilon_Nagakura.2ti', ax,
                       label=r'Carboneto $\epsilon$', lw=1.2, color='b')
    plot_indexed_peaks('eta_Hirotsu.2ti', ax,
                       label=r'Carboneto $\eta$', lw=1.2, color='r')

    ax.legend(loc=9, bbox_to_anchor=(0.5, -0.12), ncol=3, fancybox=False)

    fig.savefig('selected_diffractograms_eta.pdf', bbox_inches='tight')

    plt.show()
