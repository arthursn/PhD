#!/bin/bash

mogrify -format jpg *.tif
mogrify -crop 645x480+0+0 *.jpg

mogrify -format pdf *.jpg
