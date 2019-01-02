#!/usr/bin/env Rscript

setQT <- c(140,170,200)
setPT <- c(200,250,300,375,450)

directory <- "data/"

png("wC_alpha.png", height=2000, width=2300, res=400)

par(mar=c(3,3,0,0))
plot(c(0,900),c(0,.8),type="n")
mtext("Tempo de partição [s]", side=1, line=2)
mtext(expression(paste("% de carbono dissolvido em ",alpha)), side=2, line=2)
grid()

col <- 0
lty <- 0
legenda <- 0

i <- 1
for (PT in setPT) {
	if (PT == 450)
		i <- 6
	j <- 1
	if(PT == 375)
		setQT <- c(140,170)
	else if(PT==450)
		setQT <- c(140,170)
	else
		setQT <- c(140,170,200)

	for (QT in setQT) {
		filename <- paste("f_aTT",QT,"TP",PT,".dat",sep="")
		f_a <- read.table(paste(directory,filename,sep=""))

		filename <- paste("wCTT",QT,"TP",PT,".dat",sep="")
		wC <- read.table(paste(directory,filename,sep=""))

		x0 <- .757
		wC$V2 <- wC$V2 + x0
		var <- (x0 - wC$V2*(1-f_a$V2))/f_a$V2

		points(f_a$V1,var,col=i, lty=j,type="l")

		col <- c(col,i)
		lty <- c(lty,j)
		legenda <- c(legenda,paste("TT=",QT,"°C & TP=",PT,"°C",sep=""))

		j <- j + 1
	}
	i <- i + 1
}

col <- col[-1]
lty <- lty[-1]
legenda <- legenda[-1]

legend("bottomleft", legenda, col=col, lty=lty, bty="n", cex=.9)
graphics.off()