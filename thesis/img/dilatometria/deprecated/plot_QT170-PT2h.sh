#!/bin/bash

gnuplot << TOEND

set encoding utf8
set terminal postscript eps color enhanced "Helvetica" 24

#################### dl x t during partitiong step ###################
set output 'dlxt_PT.eps'

set yrange [-.1:.5]
set xrange [0:120]
set xlabel "Tempo de partição [min]"
set ylabel "Dilatação relativa ({/Symbol D}L/L_0) [%]" offset 2
set grid
set key invert
set size 1.2,1.2

files = system("ls -r /home/arthur/Copy/Dilatometria/Arthur_Nishikawa/FoFo_QP-2h/PT/x*.asc")
title = "450oC/2h 375oC/2h 300oC/2h 250oC/2h 200oC/2h"
pt = "1 2 3 8 6 12"
pc = "7 1 2 3 4 9"

plot for [i=1:5] word(files,i) u (\$2/60):(\$4*100/10e3) ev 5 t "TP=".word(title,i) lt word(pt,i) lc word(pc,i)

#################### dl x t during partitiong step (inset) ###################
set output 'dlxt_PT-inset.eps'

set xlabel ""
set ylabel ""
set yrange [-.05:.15]
set xrange [0:5]
set size .6,.5
unset key

plot for [i=1:5] word(files,i) u (\$2/60):(\$4*100/10e3) t word(title,i) lt word(pt,i) lc word(pc,i)

#################### dl x T during quenching, partitioning and final cooling ###################
set output 'dlxT_qPTfc.eps'
set xrange [0:470]
set yrange [-.3:.8]
set size 1.2,1.2
set xlabel "Temperatura [{/Symbol \260}C]"
set ylabel "Dilatação relativa ({/Symbol D}L/L_0) [%]"
set grid
set key invert left

files = system("ls -r /home/arthur/Copy/Dilatometria/Arthur_Nishikawa/FoFo_QP-2h/quenching_PT_f-cooling/x*.asc")
plot for [i=1:5] word(files,i) u 3:(\$4*100/10e3) t "TP=".word(title,i) lt word(pt,i) lc word(pc,i)


TOEND
