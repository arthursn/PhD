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

for fname in glob.glob('0/*bmp') + glob.glob('5min/*bmp'):
    if os.path.isfile(fname):
        fout = '{}.pdf'.format(os.path.splitext(fname)[0])

        print(fname)

        basename = fname.split('/')[-1]
        basename = basename.split('.')[0]
        
        mag = basename.split('x')[0].replace('k', 'e3')
        mag = float(mag)/1e3
        pxsize = pxsize1kx/mag

        # open and convert to grayscale
        img = Image.open(fname).convert('LA')
        img = img.crop(box=(161,0,1119,958))
        plt.imshow(img)

        scalebar = ScaleBar(pxsize*1e-6, length_fraction=.3, location='lower left')
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
