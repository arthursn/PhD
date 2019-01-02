#!/usr/bin/env Rscript

library(fields)

data <- read.table("/home/arthur/Copy/XTMS/XTMS_mai-2015/Resultados_FoFo/QP/raw_Mythen/FoFo_PT250-2h.mythen")
tth <- data$V1[1:2560]
I <- matrix(data$V3,nrow=2560)
I.sums <- colSums(I)
I.n <- t(t(I)/I.sums)
I <- I.n
time <- (0:(ncol(I)-1))*3.5/60


png("map_TT170TP250.png",width=2000, height=1200,res=200)
par(mar=c(3,3,2,2))
image.plot(tth,time,I**0.5,xlab="",ylab="")
title("")
mtext(side=1,line=2,expression(paste(2*theta, " [°]")))
mtext(side=2,line=2,"Tempo de partição [min]")
mtext(side=4,line=5,expression("Intensidade normalizada"^"0,5"))

png("map_TT170TP250_2.png",width=2000, height=1200,res=250)
par(mar=c(3,3,2,2))
image.plot(tth,time,I**0.5,xlab="",ylab="",xlim=c(28,30.5))
title("")
mtext(side=1,line=2,expression(paste(2*theta, " [°]")))
mtext(side=2,line=2,"Tempo de partição [min]")
mtext(side=4,line=5,expression("Intensidade normalizada"^"0,5"))

source("/home/arthur/Copy/XTMS/macros.R")
par(mar=c(3,3,1,1))
png("map_TT170TP250_waterfall.png",width=2000, height=1500,res=250)
waterfallPlot(I=I.n,tth=tth, each=20, scale=20, y=time, ylim=c(0,130), ylab="Tempo de partição [min]")

graphics.off()

