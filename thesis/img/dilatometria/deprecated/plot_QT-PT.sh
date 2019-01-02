#!/bin/bash

gnuplot << TOEND

set encoding utf8
set terminal postscript eps color enhanced "Helvetica" 24

#################### dl x t for different QT and PT=375 ###################
set output 'dlxt_PT375.eps'

set xrange [0:15]
set yrange [-.05:.45]
set xlabel "Tempo [min]"
set ylabel "Dilatação relativa ({/Symbol D}L/L_0) [%]"
set grid
set key left
set size 1.2,1.

files = system("ls data/PT/*-375-PT.asc")
title = "TT=140oC TT=170oC TT=200oC"
pt = "1 2 3 8"
pc = "7 1 2 3"
plot "data/austempera/375.asc" u (\$2/60):3 ev 2 t "Austêmpera a 375oC" lt 8 lc 3, for [i=1:3] word(files,i) u (\$2/60):3 ev 2 t word(title,i)." PT=375oC" lt word(pt,i) lc word(pc,i)

#################### dl x t for different QT and PT=300 ###################
set output 'dlxt_PT300.eps'
set yrange [-.05:.5]
set key left

files = system("ls data/PT/*-300-PT.asc")
plot "data/austempera/300.asc" u (\$2/60):3 ev 2 t "Austêmpera a 300oC" lt 8 lc 3, for [i=1:3] word(files,i) u (\$2/60):3 ev 2 t word(title,i)." PT=300oC" lt word(pt,i) lc word(pc,i)

#################### dl x t for different QT and PT=250 ###################
set output 'dlxt_PT250.eps'
set yrange [0:.35]
set key right

files = system("ls data/PT/*-250-PT.asc")
plot "data/austempera/250.asc" u (\$2/60):3 ev 2 t "Austêmpera a 250oC" lt 8 lc 3, for [i=1:3] word(files,i) u (\$2/60):3 ev 2 t word(title,i)." PT=250oC" lt word(pt,i) lc word(pc,i)

#################### dl x t for austempering ###################
set output 'dlxt_austempera.eps'
set yrange [-.05:.5]
set key left invert
pt = "1 2 3 8 6 12"
pc = "7 1 2 3 4 9"
title = "450oC 375oC 300oC 250oC 200oC"

files = system("ls -r data/austempera/*.asc")
plot for [i=1:5] word(files,i) u (\$2/60):3 ev 2 t word(title,i) lt word(pt,i) lc word(pc,i)

TOEND
