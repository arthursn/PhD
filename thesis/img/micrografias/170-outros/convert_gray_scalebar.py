import glob
import os
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.font_manager import FontProperties

from PIL import Image
from matplotlib_scalebar.scalebar import ScaleBar

font0 = FontProperties()
font0.set_size(13)
font0.set_family('sans-serif')
font0.set_file('/usr/share/fonts/truetype/msttcorefonts/Arial.ttf')

pxsize1kx = 20./214.

# fname: px size (um)
cal = {'6a.png': pxsize1kx/10.,
       '6b.png': 10./304.,
       '6d.png': pxsize1kx/10.,
       '6d-2.png': pxsize1kx/10.,
       '6e.png': pxsize1kx/5.}

for fname, pxsize in cal.items():
    if os.path.isfile(fname) is True:
        fout = '{}.pdf'.format(os.path.splitext(fname)[0])

        print(fname)

        basename = fname.split('/')[-1]
        basename = basename.split('.')[0]

        # open and convert to grayscale
        img = Image.open(fname)  # .convert('LA')
        plt.imshow(img)

        scalebar = ScaleBar(pxsize*1e-6, location='lower left')
        scalebar.font_properties = font0
        plt.gca().add_artist(scalebar)

        plt.gca().set_axis_off()
        plt.subplots_adjust(top=1, bottom=0, right=1,
                            left=0, hspace=0, wspace=0)
        plt.margins(0, 0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())

        plt.savefig(fout, bbox_inches='tight', pad_inches=0, dpi=300)

        plt.close()
