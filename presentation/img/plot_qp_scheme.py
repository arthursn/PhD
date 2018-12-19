# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


dt, T = np.array([[0, 0],
                  [2, 880],
                  [5, 880],
                  [1, 170],
                  [2, 170],
                  [.4656, 375],
                  [3, 375],
                  [.5282, 0]]).T
t = np.cumsum(dt)

fig, ax = plt.subplots()
line, = ax.plot(t, T, color='.8')

dt, T = np.array([[0, 0],
                  [2, 880],
                  [5, 880],
                  [1, 170],
                  [2, 170],
                  [.2394, 0]]).T
t = np.cumsum(dt)


line, = ax.plot(t, T, color='k', lw=1.5)

plt.show()
