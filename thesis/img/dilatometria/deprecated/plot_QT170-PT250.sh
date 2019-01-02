#!/bin/bash

gnuplot << TOEND

set encoding utf8
set terminal postscript eps color enhanced "Helvetica" 24

set ytics nomirror
set y2tics nomirror

set xlabel "Tempo [min]"
set ylabel "Dilatação relativa [%]" offset 2
set y2label "Temperatura [°C]" offset -1
set grid
set size 1.2,1.

file = "/home/arthur/Copy/Dilatometria/Arthur_Nishikawa/FoFo_QP-2h/1_fofo_Q&P_PT170-QT250-2h_05.05.15.asc"

set output "170-250.eps"

plot file u (\$2/60):(\$4*100/10e3) w l ax x1y1 lw 2 lc 0 lt 1 t "Dilatação", "" u (\$2/60):3 w l ax x1y2 lc 0 lt 2 lw 2 t "Temperatura"

set output "170-250_close.eps"
set xrange [30:35]
set yrange [-.2:.4]
set y2range [0:400]

replot

TOEND
#data <- read.table("~/Dropbox/Dilatometria/2014-05-16/170-300.asc")
#png("170-300.png", width=1800, height=1500, res=300)
#par(mar=c(3,3,1,3))
#plot(V3~V2, data, type="l", xlab="", ylab="")
#mtext("Tempo [s]", side=1, line=2)
#mtext("Dilatação relativa [%]", side=2, line=2)
#par(new=TRUE)
#plot(V4~V2, data, type="l", axes=FALSE, lty=2, xlab="", ylab="")
#axis(4)
#mtext("Temperatura [°C]", side=4, line=2)
#dev.off()
#
#png("170-300_close.png", width=1800, height=1500, res=300)
#par(mar=c(3,3,1,3))
#plot(V3~V2, data, type="l", xlab="", ylab="", xlim=c(1800,2000), ylim=c(-.5,.5))
#mtext("Tempo [s]", side=1, line=2)
#mtext("Dilatação relativa [%]", side=2, line=2)
#par(new=TRUE)
#plot(V4~V2, data, type="l", axes=FALSE, lty=2, xlab="", ylab="", xlim=c(1800,2000), ylim=c(0,400))
#axis(4)
#mtext("Temperatura [°C]", side=4, line=2)
#dev.off()
