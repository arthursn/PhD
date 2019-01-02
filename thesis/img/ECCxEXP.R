#/usr/bin/env Rscript

ERC <- read.table("ERC.dat", header=TRUE)
exp <- read.table("f_g.dat", header=TRUE)

TP <- c(200,250,300,375,450)

png("ERCxEXP.png", width=2000, height=1500, res=400)
par(mar=c(3,3,0,0))
plot(100*f_g~TT, data=ERC, xlab="", ylab="", type="n", ylim=c(0,70))
mtext("Temperatura de têmpera [°C]", side=1, line=2)
mtext("% de austenita após T&P", side=2, line=2)
grid()
points(100*f_g~TT, data=ERC, type="l", lwd=2)

for(j in 1:length(TP)) {
	if(j==5) {
		points(exp$TT[exp$TP==TP[j]], exp$f_g[exp$TP==TP[j]], type="p", pch=j, col=j+1)
		points(exp$TT[exp$TP==TP[j]], exp$f_g[exp$TP==TP[j]], type="l", pch=j, col=j+1)
	} else {
		points(exp$TT[exp$TP==TP[j]], exp$f_g[exp$TP==TP[j]], type="p", pch=j, col=j)
		points(exp$TT[exp$TP==TP[j]], exp$f_g[exp$TP==TP[j]], type="l", pch=j, col=j)
	}
}

legend("topleft", c("Previsão ERC", paste("TP=", TP,"°C", sep="")), col=c(1,1:4,6), pch=c(-1,1:5), lwd=c(2,rep(1,5)), lty=1, bty="n")
graphics.off()
