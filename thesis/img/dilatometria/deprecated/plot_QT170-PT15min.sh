#!/bin/bash

gnuplot << TOEND

set encoding utf8
set terminal postscript eps color enhanced "Helvetica" 24

#################### dl x T during quenching, partitioning and final cooling ###################
set output 'dlxT_qPT15min-fc.eps'

set xrange [0:470]
set yrange [-.3:.8]
set size 1.2,1.2
set xlabel "Temperatura [{/Symbol \260}C]"
set ylabel "Dilatação relativa ({/Symbol D}L/L_0) [%]"
set grid
set key invert left
set size 1.2,1.2

files = system("ls -r data/170*.asc")
title = "450oC/15min 375oC/15min 300oC/15min 250oC/15min 200oC/15min"
pt = "1 2 3 8 6"
pc = "7 1 2 3 4"
l0 = ".051 .021 -.260 -.008 -.337"

plot for [i=1:5] word(files,i) u 4:(\$3-word(l0,i)) ev 2::3000 t "TP=".word(title,i) lt word(pt,i) lc word(pc,i)


TOEND
