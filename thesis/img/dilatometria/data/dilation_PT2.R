setQT <- c(140,170,200)
setPT <- c(200,250,300,375,450)
#setPT <- c(375,450)
#setPT <- c(300)

Ta <- 880

directory <- "data/"

par(mar=c(3,3,0,0))
plot(c(0,1)~c(0,1),type="n",xlim=c(0,15*60),ylim=c(-1,2),xlab="",ylab="")
grid()
mtext("Tempo de partição [s]", side=1, line=2)
mtext("Dilatação relativa corrigida [%]", side=2, line=2)

i <- 1
for (PT in setPT) {
	j <- 1
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
		dil <- (dil-dil[1])/(dil[length(dil)] - dil[1])

		points(dil~t,type="l",lty=j,col=i,lwd=2)
		j <- j + 1
	}
	i <- i + 1
}