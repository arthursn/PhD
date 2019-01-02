#!/usr/bin/env Rscript

IT <- c(200,250,300,375,450)
Ta <- 880

directory <- "data/"

png("dilation_IBT.png",width=2000, height=1800,res=400)
par(mar=c(3,3,0,0))
plot(c(0,1)~c(0,1),type="n",xlim=c(0,15*60),ylim=c(0,0.5),xlab="",ylab="")
mtext("Tempo de austêmpera [s]", side=1, line=2)
mtext("Dilatação relativa corrigida [%]", side=2, line=2)
grid()
for (j in 1:length(IT)) {
	t0 <- Ta/10 + 30*60 + (880-IT[j])/50 + 1

	filename <- paste(IT[j],".asc",sep="")
	var <- read.table(paste(directory,filename,sep=""))

	t <- 0
	dil <- 0
	T <- 0
	for (k in 1:length(var$V1)) {
		if (var$V2[k] >= t0) {
			t <- c(t,var$V2[k])
			dil <- c(dil,var$V3[k])
			T <- c(T,var$V4[k])
		}
	}

	t <- t[-1]
	t <- t-t0
	dil <- dil[-1]
	dil <- (dil-dil[1])
	T <- T[-1]

	points(dil[1:1000]~t[1:1000],type="l",lty=j)
}
legend("topleft", c("200°C","250°C","300°C","375°C","450°C"), lty=1:5, bty="n")
graphics.off()

