setQT <- c(140,170,200)
#setPT <- c(200,250,300,375,450)
#setPT <- c(375,450)
setPT <- c(300)

Ta <- 880

directory <- "data/"

for (PT in setPT) {
	filename <- paste("dilxtime_PT",PT,".png",sep="")
	#png(filename,width=2000, height=2000,res=450)
	par(mar=c(3,3,0,0))
	plot(c(0,1)~c(0,1),type="n",xlim=c(0,15*60),ylim=c(-.1,0.4),xlab="",ylab="")
	grid()
	mtext("Tempo de partição [s]", side=1, line=2)
	mtext("Dilatação relativa corrigida [%]", side=2, line=2)
	j <- 1
	#if(PT == 375 || PT == 450)
		#setQT <- c(140,170)
	for (QT in setQT) {
		ti <- Ta/10 + 30*60 + (880-QT)/50 + 60 + (PT-QT)/10
		tf <- ti + 15*60

		filename <- paste(QT,"-",PT,".asc",sep="")

		var <- read.table(paste(directory,filename,sep=""))

		t <- 0
		dil <- 0
		for (k in 1:length(var$V1)) {
			if (var$V2[k] >= ti) {
				if (var$V2[k] <= tf) {
					t <- c(t,var$V2[k])
					dil <- c(dil,var$V3[k])
				}
			}
		}

		t <- t[-1]
		t <- t-ti
		dil <- dil[-1]
		dil <- (dil-dil[1])

		points(dil~t,type="l",lty=j,cex=.5)
		j <- j + 1
	}
	legend("topleft", paste("TT=", setQT, "°C & TP=", PT, "°C", sep=""), lty=1:3, bty="n")
	#graphics.off()
}

#legend("topleft", paste("QT=", rep(c(140,170,200),3), "°C & PT=", rep(c(200,250,300),each=3), "°C", sep=""), col=rep(1:3,each=3), lty=rep(1:3,3), bg="white")
#dev.off()