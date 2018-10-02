#!/usr/bin/python3

# -*- coding: utf-8 -*-

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from cpartition import x2wp, CProfiles


def label_mart_CCE(ax):
    artists = []

    artists += [ax.text(-.91, -.05, r"$\alpha'$", ha='center', va='top')]
    artists += [ax.text(-.33, -.05, r"$\gamma$", ha='center', va='top')]
    artists += [ax.text(.33, -.05, r"$\gamma$", ha='center', va='top')]
    artists += [ax.text(.91, -.05, r"$\alpha'$", ha='center', va='top')]

    artists += [ax.axhline(0.76, ls=':', color='k')]
    artists += [ax.text(1.16, .76, r'$c_0$', ha='right', va='bottom')]

    return artists


def label_mart_CCEtheta(ax):
    artists = []

    artists += [ax.text(-.91, -.05, r"$\alpha' + \theta$",
                        ha='center', va='top')]
    artists += [ax.text(-.5, -.05, r"$\gamma$", ha='center', va='top')]
    artists += [ax.text(.5, -.05, r"$\gamma$", ha='center', va='top')]
    artists += [ax.text(.91, -.05, r"$\alpha' + \theta$",
                        ha='center', va='top')]

    artists += [ax.axhline(0.76, ls=':', color='k')]
    artists += [ax.text(1.16, .76, r'$c_0$', ha='right', va='bottom')]

    return artists


def label_coupled_CCE(ax):
    artists = []

    artists += [ax.text(-.91, -.05, r"$\alpha'$", ha='center', va='top')]
    artists += [ax.text(-.5, -.05, r"$\gamma$", ha='center', va='top')]
    artists += [ax.text(-.33, -.05, r"$\alpha_b$", ha='center', va='top')]
    artists += [ax.text(-.166, -.05, r"$\gamma$", ha='center', va='top')]
    artists += [ax.text(-0, -.05, r"$\alpha_b$", ha='center', va='top')]
    artists += [ax.text(.166, -.05, r"$\gamma$", ha='center', va='top')]
    artists += [ax.text(.33, -.05, r"$\alpha_b$", ha='center', va='top')]
    artists += [ax.text(.5, -.05, r"$\gamma$", ha='center', va='top')]
    artists += [ax.text(.91, -.05, r"$\alpha'$", ha='center', va='top')]

    artists += [ax.axhline(1.59022, ls=':', color='k')]
    artists += [ax.text(1.16, 1.59022, 'WBs', ha='right', va='bottom')]

    artists += [ax.axhline(0.76, ls=':', color='k')]
    artists += [ax.text(1.16, .76, r'$c_0$', ha='right', va='bottom')]

    return artists


def label_coupled_CCEtheta(ax):
    artists = []

    artists += [ax.text(-.91, -.05, r"$\alpha' + \theta$",
                        ha='center', va='top')]
    artists += [ax.text(-.5, -.05, r"$\gamma$", ha='center', va='top')]
    artists += [ax.text(-.33, -.05, r"$\alpha_b$", ha='center', va='top')]
    artists += [ax.text(-.166, -.05, r"$\gamma$", ha='center', va='top')]
    artists += [ax.text(-0, -.05, r"$\alpha_b$", ha='center', va='top')]
    artists += [ax.text(.166, -.05, r"$\gamma$", ha='center', va='top')]
    artists += [ax.text(.33, -.05, r"$\alpha_b$", ha='center', va='top')]
    artists += [ax.text(.5, -.05, r"$\gamma$", ha='center', va='top')]
    artists += [ax.text(.91, -.05, r"$\alpha' + \theta$",
                        ha='center', va='top')]

    artists += [ax.axhline(1.59022, ls=':', color='k')]
    artists += [ax.text(1.16, 1.59022, 'WBs', ha='right', va='bottom')]

    artists += [ax.axhline(0.76, ls=':', color='k')]
    artists += [ax.text(1.16, .76, r'$c_0$', ha='right', va='bottom')]

    return artists


class CPartitionAnimation(object):

    # Site fraction of substitutional elements in the ductile cast iron
    yalloy = dict(Cu=3.55354266E-3, Mn=2.05516602E-3,
                  Si=5.02504411E-2, Fe=9.4414085022e-1)

    def __init__(self, basename, time, **kwargs):
        # Required arguments
        self.basename = basename
        self.time = time

        # Optional arguments
        self.directory = kwargs.pop('directory', 'C_profiles')
        self.xlim = kwargs.pop('xlim', None)
        self.ylim = kwargs.pop('ylim', None)
        self.title = kwargs.pop('title', None)
        self.mirror = kwargs.pop('mirror', True)
        self.callback = kwargs.pop('callback', None)

        # Instantiate CProfiles and load carbon profiles
        self.cprofiles = CProfiles(self.basename, self.directory)
        self.cprofiles.load_cprofiles()
        self.cprofiles.load_time()

        self.time_idx = self.cprofiles.where_tlist(self.time, appendto=[])

        # Matplotlib Figure object
        self.fig, self.ax = plt.subplots(**kwargs)

        # Plotting options
        self.ax.set_xlabel(u'Posição ' + r'($\mu m$)')
        self.ax.set_ylabel(u'Teor de carbono (% peso)')
        self.ax.set_xlim(self.xlim)
        self.ax.set_ylim(self.ylim)
        if self.title:
            self.ax.set_title(self.title)

        self.ani = None

        self.artists = []

        # Run callback function
        if self.callback is not None:
            self.artists += self.callback(self.ax)

    def x2wp(self, x):
        return x2wp(x, y=self.yalloy)

    def initialize_plot(self):
        self.tprevious = 0

        i = self.time_idx[0]
        z, c, t = self.cprofiles.get_cprofile(i, self.mirror, self.x2wp)

        self.line, = self.ax.plot(z, c, 'k-')
        self.time_text = self.ax.text(0.02, 0.98, '', va='top',
                                      transform=self.ax.transAxes)

        axis = ''
        if self.xlim is None:
            axis += 'x'
        if self.ylim is None:
            axis += 'y'
        axis = axis.replace('xy', 'both')

        if axis:
            self.ax.autoscale(True, axis=axis, tight=True)
            self.ax.autoscale(False)

        return [self.line, self.time_text] + self.artists

    def plot_step(self, *args):
        z, c, t = args[0]

        spf = t - self.tprevious  # seconds per frame
        self.tprevious = t

        self.line.set_data(z, c)

        string = 't = {:g} s'.format(t)
        string += '\n'
        string += '{:g} s / quadro'.format(spf)

        self.time_text.set_text(string)

        return [self.line, self.time_text] + self.artists

    def frames(self):
        for i in self.time_idx:
            z, c, t = self.cprofiles.get_cprofile(i, self.mirror, self.x2wp)

            yield z, c, t

    def animate(self, **kwargs):
        kw = dict(interval=25, blit=True)
        kw.update(kwargs)
        self.ani = animation.FuncAnimation(fig=self.fig,
                                           func=self.plot_step,
                                           frames=self.frames,
                                           init_func=self.initialize_plot,
                                           **kw)
        return self.ani

    def save_animation(self, fout=None, directory='', **kwargs):
        if self.ani is not None:
            try:
                if fout is None:
                    fout = os.path.join(
                        directory, self.cprofiles.basename) + '.mp4'
                self.ani.save(fout, **kwargs)
            except:
                raise
            else:
                print('Animation successfully saved in "{}"'.format(fout))
        else:
            print('Run animate() first')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('basenames', nargs='+')
    parser.add_argument('-t', '--time', type=float, nargs=3,
                        required=True, help='ti tf tstep')

    parser.add_argument('-i', '--interval', type=float, default=25)

    parser.add_argument('-m', '--mirror', action='store_true')
    parser.add_argument('-f', '--figsize', type=float, nargs=2, default=[6, 4])
    parser.add_argument('-x', '--xlim', type=float,
                        nargs=2, default=None)
    parser.add_argument('-y', '--ylim', type=float,
                        nargs=2, default=None)
    parser.add_argument('-T', '--title', default=None)

    parser.add_argument('-s', '--silent', action='store_false')
    parser.add_argument('-S', '--save', action='store_true')
    parser.add_argument('-d', '--dpi', default=300)

    args = parser.parse_args()

    directory = '/home/arthur/repositories/cpartition_simulations/C_profiles'

    for basename in args.basenames:
        time = np.arange(args.time[0], args.time[1], args.time[2])

        if 'mart' in basename:
            if 'CCEpara' in basename or 'CCEortho' in basename or 'mu' in basename:
                callback = label_mart_CCEtheta
            else:
                callback = label_mart_CCE
        else:
            if 'CCEpara' in basename or 'CCEortho' in basename or 'mu' in basename:
                callback = label_coupled_CCEtheta
            else:
                callback = label_coupled_CCE

        cpartition = CPartitionAnimation(basename=basename,
                                         directory=directory,
                                         time=time,
                                         callback=callback,
                                         figsize=args.figsize,
                                         xlim=args.xlim,
                                         ylim=args.ylim,
                                         title=args.title,
                                         mirror=args.mirror)
        cpartition.animate(interval=args.interval)

        if args.save:
            cpartition.save_animation(dpi=args.dpi)

    if args.silent:
        plt.show()
