#!/usr/bin/env Rscript

data <- read.table("data/57_fofo_QP.d01-step011-S-11-mythen")

png("finalScan.png", width=2000, height=1800, res=400)
par(mar=c(3,3,1,0))
plot(V3~V1,data,type="h",xlab="",ylab="", ylim=c(0,1e4))
mtext(expression(2*theta), side=1, line=2)
mtext("Intensidade", side=2, line=2)
graphics.off()