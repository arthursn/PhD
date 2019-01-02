import numpy as np

def add_label(ax, label, px=.15, py=.1, size=20):
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    x = float(min(xlim) - np.diff(xlim)*px)
    y = float(max(ylim) + np.diff(ylim)*py)
    ax.text(x=x, y=y, s=label, size=size)

def load_big_file(fname, ncol=None, nrow=None):
    import time
    t0 = time.time()
    if ncol == None or nrow == None:
        rows = []
        with open(fname) as f:
            for line in f:
                if line[0] == '#' or line == '\n':
                    pass
                else:
                    line = [float(s) for s in line.split()]
                    rows.append(np.array(line, dtype = np.double))
        x = np.vstack(rows)  # convert list of vectors to array
    else:
        x = np.empty((int(nrow), int(ncol)), dtype = np.double)
        with open(fname) as f:
            irow = 0
            for line in f:
                if irow >= nrow:
                    print('Number of rows exceed informed value.')
                    break
                if line[0] == '#' or line == '\n':
                    pass
                else:
                    for icol, s in enumerate(line.split()):
                        x[irow, icol] = float(s)
                    irow += 1
    print('Time elapsed: {:.2f} s'.format(time.time() - t0))
    return x

def test_ptime(fname):
    import time
    t0 = time.time()
    a = load_big_file(fname)
    print('load_big_file: {:.4f} s'.format(time.time() - t0))

    t0 = time.time()
    b = np.loadtxt(fname)
    print('loadtxt: {:.4f} s'.format(time.time() - t0))

    return (a, b)
