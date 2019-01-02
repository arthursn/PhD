directory <- "data/"
QT <- 170
PT <- 250
Ta <- 880

#data <- read.table(paste(directory,filename,sep=""))
#png("170-250.png", width=1800, height=1500, res=300)
#par(mar=c(3,3,1,3))
#plot(V3~V2, data, type="l", xlab="", ylab="")
#mtext("Tempo [s]", side=1, line=2)
#mtext("Dilatação relativa [%]", side=2, line=2)
#par(new=TRUE)
#plot(V4~V2, data, type="l", axes=FALSE, lty=2, xlab="", ylab="")
#axis(4)
#mtext("Temperatura [°C]", side=4, line=2)
#graphics.off()


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

png("dilxtime_170-250.png", width=1800, height=750, res=300)
par(mar=c(3,3,0,0))
plot(dil~t,type="l",xlab="",ylab="",lwd=2)
mtext("Tempo de partição [s]", side=1, line=2)
mtext("Dil. rel. corrigida [%]", side=2, line=2)
graphics.off()

###################3

ti <- Ta/10 + 30*60 + (880-QT)/50 + 60
tiso <- Ta/10 + 30*60 + (880-QT)/50 + 60 + (PT-QT)/10

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

png("dilxT_170-250.png", width=1800, height=750, res=300)
par(mar=c(3,3,0,0))
plot(dil~T,type="l",xlab="",ylab="", lwd=2)
mtext("Temperatura [°C]", side=1, line=2)
mtext("Dil. rel. corrigida [%]", side=2, line=2)
graphics.off()