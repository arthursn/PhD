alpha <- function(T) {
	#T <- T+273.15
	#B <- 18.3e-6
	#Th <- 320
	#return(103.9e-4+B*Th+B*Th*(exp(-T/Th)-1))
	return(0.17501+9.51282e-4*T)
}
gamma <- function(T) {
	#T <- T+273.15
	#B <- 24.8e-6
	#Th <- 280
	#return(B*Th+B*Th*(exp(-T/Th)-1))
	return(-0.59841+0.00187*T)

}

KM <- function(T) {
	return(exp(-0.01235*(221.069-T)))
}

###########################3
QT <- rep(c(140,170,200),each=3)
PT <- rep(c(200,250,300),3)
dil0 <- (alpha(PT)-gamma(PT))/100
f_g0 <- KM(QT)

Ta <- 880

directory <- "~/Dropbox/Dilatometria/2014-05-16/"

png("~/Desktop/dil-kinetics.png",width=2000, height=2000,res=300)
#plot(c(0,1)~c(0,1),type="n",xlim=c(0,15*60),ylim=c(0,1),xlab="Time [s]",ylab=expression(f[alpha*"-iso"]==f[alpha]-f[alpha*"'"]))
plot(c(0,1)~c(0,1),type="n",xlim=c(0,15*60),ylim=c(0,1),xlab="Time [s]",ylab=expression(f[alpha]))
#for (j in 1:length(QT)) {
	j <- 9
	{
	#if(QT[j] != PT[j]) {
		t0 <- Ta/10 + 30*60 + (880-QT[j])/50 + 60 + (PT[j]-QT[j])/10
	#} else {
	#	t0 <- Ta/10 + 30*60 + (880-QT[j])/50
	#}

	filename <- paste(QT[j],"-",PT[j],".asc",sep="")

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
	dil <- (dil-dil[1])/100
	T <- T[-1]

	points((dil*f_g0[j]/(dil0[j])+1-f_g0[j])~t,type="l",lty=ceiling(j/3), col=((j-1)%%3+1), lwd=2)

	#print(t0)
}
#legend("topleft", paste("QT=", rep(c(140,170,200),3), "°C & PT=", rep(c(200,250,300),each=3), "°C", sep=""), col=rep(1:3,each=3), lty=rep(1:3,3), bg="white")
dev.off()