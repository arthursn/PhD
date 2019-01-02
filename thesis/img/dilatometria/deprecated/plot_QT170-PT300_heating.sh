#!/bin/bash

gnuplot << TOEND

set encoding utf8
set terminal postscript eps color enhanced "Helvetica" 24

#################### dl x T during quenching, partitioning and final cooling ###################
set output 'dlxt_heating.eps'

set xrange [0:15]
set yrange [0:.3]
set size 1.2,1.2
set xlabel "Tempos [min]"
set ylabel "Dilatação relativa ({/Symbol D}L/L_0) [%]"
set grid
set key left
set size 1.2,1.2

pt = "1 2"
pc = "7 1"

#plot for [i=1:5] word(files,i) u 4:(\$3-word(l0,i)) ev 2::3000 t "TP=".word(title,i) lt word(pt,i) lc word(pc,i)

plot 'data/PT/170-300-PT.asc' u (\$2/60):3 t "TT=170oC & TP=300oC, {/Symbol F} = 10oC/s" lt 1 lc 7, 'data/PT/170-300_heating50oCs-1-PT.asc' u (\$2/60):6 t "TT=170oC & TP=300oC, {/Symbol F} = 50oC/s" lt 2 lc 1


TOEND
