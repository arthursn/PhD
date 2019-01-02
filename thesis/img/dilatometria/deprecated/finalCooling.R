setQT <- c(140,170,200)
#setPT <- c(200,250,300,375,450)
setPT <- c(375,450)

dilRange <- function(PT) {
	output <- NA
	if (PT==200)
		output <- c(-.2,.3)
	else if (PT==250)
		output <- c(-.4,.4)
	else if (PT==300)
		output <- c(-.4,.5)
	else if (PT==375)
		output <- c(-.6,.3)
	else if (PT==450)
		output <- c(-.8,.2)

	return(output)
}

Ta <- 880

directory <- "data/"

for (PT in setPT) {
	filename <- paste("dilxT_PT",PT,".png",sep="")
	png(filename,width=2000, height=2000,res=450)
	par(mar=c(3,3,0,0))
	plot(c(0,1)~c(0,1),type="n",xlim=c(0,PT+50),ylim=dilRange(PT),xlab="",ylab="")
	grid()
	mtext("Temperatura [°C]", side=1, line=2)
	mtext("Dilatação relativa corrigida [%]", side=2, line=2)
	j <- 1
	#if(PT == 375 || PT == 450)
		#setQT <- c(140,170)
	for (QT in setQT) {
		ti <- Ta/10 + 30*60 + (880-QT)/50 + 60
		tiso <- Ta/10 + 30*60 + (880-QT)/50 + 60 + (PT-QT)/10

		filename <- paste(QT,"-",PT,".asc",sep="")

		var <- read.table(paste(directory,filename,sep=""))

		dil <- 0
		T <- 0
		diliso <- 0
		for (k in 1:length(var$V1)) {
			if (var$V2[k] >= ti) {
				dil <- c(dil,var$V3[k])
				T <- c(T,var$V4[k])
				if (var$V2[k] >= tiso) {
					diliso <- c(diliso,var$V3[k])
				}
			}
		}

		dil <- dil[-1]
		dil <- (dil-diliso[2])
		T <- T[-1]

		#points(dil~T,type="l",lty=ceiling(j/3), col=((j-1)%%3+1))
		points(dil~T,type="l",lty=j)
		j <- j + 1
	}
	legend("topleft", paste("TT=", setQT, "°C & TP=", PT, "°C", sep=""), lty=1:3, bty="n")
	graphics.off()
}