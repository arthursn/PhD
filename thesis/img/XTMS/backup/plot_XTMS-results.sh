#!/bin/bash

gnuplot << TOEND
# Setting the terminal postscript with the options
set encoding utf8
set terminal postscript eps color enhanced "Helvetica" 24

#################### DwC x t during partitiong step ###################

set output "DwC_QP.eps"

set yrange [0:1.2]
set xrange [0:120]

set xlabel "Tempo de partição [min]"
set ylabel "{/Symbol D} %wt C" offset 2
set grid
set size 1.2,1.2

files = system("ls /home/arthur/Copy/XTMS/XTMS_mai-2015/Resultados_FoFo/QP/DwC/*.dat")
title = "200oC/2h 250oC/2h 300oC/2h 375oC/2h 450oC/2h "
pt = "1 2 3 8 6 12"
pc = "7 1 2 3 4 9"

plot for [i=1:5] word(files,i) u (\$2/60):3 ev 3 t "TP=".word(title,i) lt word(pt,i) lc word(pc,i)

#################### f_alpha x t during partitiong step ###################

set output "f_alpha-iso_QP.eps"
set ylabel "Fração de {/Symbol a} isotérmico (f_{{/Symbol a}-iso})" offset 2
set yrange [0:.75]
set size 1.2,1

files = system("ls /home/arthur/Copy/XTMS/XTMS_mai-2015/Resultados_FoFo/QP/f_phase/*.dat")
plot for [i=1:5] word(files,i) u (\$2/60):5 ev 3 t "TP=".word(title,i) lt word(pt,i) lc word(pc,i)

#################### f_gamma x t during partitiong step ###################

set output "f_gamma_QP.eps"
set ylabel "Fração de austenita (f_{/Symbol g})" offset 2
set yrange [0:.6]
set size 1.2,1

files = system("ls /home/arthur/Copy/XTMS/XTMS_mai-2015/Resultados_FoFo/QP/f_phase/*.dat")
plot for [i=1:5] word(files,i) u (\$2/60):3 ev 3 t "TP=".word(title,i) lt word(pt,i) lc word(pc,i)

TOEND

