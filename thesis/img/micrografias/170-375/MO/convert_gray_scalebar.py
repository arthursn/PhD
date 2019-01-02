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


# fname: px size (um)
# cal = {'Q170-1min/5kx-4.png': pxsize1kx/5.}
pxsize = 0.0288549241*2

for fname in glob.glob('original/*1000x.jpg'):
    if os.path.isfile(fname) is True:
        fout = '{}_scalebar.pdf'.format(os.path.splitext(fname)[0])

        print(fname + ' > ' + fout)

        basename = fname.split('/')[-1]
        basename = basename.split('.')[0]

        # open and convert to grayscale
        img = Image.open(fname)  # .convert('LA')
        plt.imshow(img)

        scalebar = ScaleBar(pxsize*1e-6, location='lower right')
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
