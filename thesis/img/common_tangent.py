import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.optimize import newton, fsolve

matplotlib.rc('font', **{'family': 'sans-serif',
                         'sans-serif': ['Arial'], 'size': 13})

fig, ax = plt.subplots(figsize=(6, 4))

ax.set_xticks([])
ax.set_yticks([])


def f(x): return 5.*(x - .1)**2.


def g(x): return 4.5*(x - .5)**2. + .5


def h(x): return f(x) + .7


def f_prime(x): return 10.*(x - .1)


def g_prime(x): return 9.*(x - .5)


x = np.linspace(0., 1., 100)
ax.plot(x, f(x), 'k-', x, g(x), 'k-', lw=1)

ax.annotate(s=r'$\alpha$', xy=(0, 0), xytext=(.1, .2), size=16)
ax.annotate(s=r'$\gamma$', xy=(0, 0), xytext=(.7, .9), size=16)

# def eqs_tg(p):
# 	a, b = p
# 	return (g(b) - f(a) - f_prime(a)*(b-a), g_prime(b) - f_prime(a))

# a, b = fsolve(eqs_tg, (0., 1.))
# print (a, b)

# ax.scatter([a,b], [f(a),g(b)], marker='|', s=100, c='k', lw=1)

# tg = lambda x: f_prime(a)*(x - a) + f(a)
# ax.plot(x, tg(x), c='k', ls='--', lw=1)
# ax.annotate(s=r'$\mu_C^\alpha = \mu_C^\gamma$', xy=(0,0), xytext=(1.01,tg(1.)))


def f0(x): return d - f(x) - (c - x)*f_prime(x)


def g0(x): return d - g(x) - (c - x)*g_prime(x)


def tg(x): return d + m*(x - c)


roman = ['I', 'II', 'III', 'IV', 'V']

for i in range(2):
    d = -.5 + .7*i
    c = .8
    ax.scatter(c, d, c='k', s=70, lw=1)
    ax.annotate(s=r'$\theta_{%s}$' % roman[i], xy=(
        0, 0), xytext=(c-.05, d-.15), size=16)

    a = newton(func=f0, x0=.1)
    ax.scatter(a, f(a), marker='|', s=100, c='k', lw=1)
    m = (d - f(a))/(c - a)
    x = np.linspace(a, 1., 100)
    ax.plot(x, tg(x), c='k', ls=':', lw=1)

    c, d = 1., tg(1.)
    a = newton(func=g0, x0=.1)
    ax.scatter(a, g(a), marker='|', s=100, c='k', lw=1)
    m = (d - g(a))/(c - a)
    x = np.linspace(a, 1., 100)
    ax.plot(x, tg(x), c='k', ls=':', lw=1)

    ax.annotate(s=r'$\mu_C^\alpha = \mu_C^{\theta_{%s}} = \mu_C^\gamma$' % roman[i], 
    	xy=(0, 0), xytext=(c+.01, d))

ax.set_ylabel('G', rotation='horizontal', ha='right')
ax.set_xlim(0., 1.)
ax.set_ylim(-.7, 1.5)
ax.set_xticks([0., 1.])
ax.set_xticklabels(['Z (Fe-X)', 'C'])
plt.savefig('common_tangent.pdf', bbox_inches='tight')
plt.show()
