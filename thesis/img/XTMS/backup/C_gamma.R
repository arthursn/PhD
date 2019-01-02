#!/usr/bin/env Rscript

g111 <- 1351
a110 <- 1840
g200 <- 644.3
a200 <- 288.6

#aplica a lei de Bragg
tth2a <- function(tth, h, k, l, lambda) {
	fator <- sqrt(h**2 + k**2 + l**2)
	a <- 0.5*lambda*fator/sin(tth*pi/360)
	return(a)
}

D_gamma <- function(T) {
	B <- 24.8e-6
	Theta <- 280
	f <- B*T + B*Theta*(exp(-T/Theta)-1)
	return(f)
}

a2C <- function(a) {
	return((a - 3.572 - 0.00157*2.47 + 0.0012*0.2)/.033)
}

directory <- "fitted/"

D_gamma0 <- D_gamma(25+273.15)
setQT <- c(140,170,200)
setPT <- c(250,300,375)

par(mar=c(3,3.2,0,0))
plot(c(0,1),c(0,1),xlim=c(0,900),ylim=c(0,1),type="n",xlab="",ylab="")
grid()
mtext("Tempo de partição [s]", side=1, line=2)
mtext(expression(paste(Delta,"%",w[C]^gamma)), side=2, line=2)

i <- 1
for (PT in setPT) {
	j <- 1
	for (QT in setQT){
		filename <- paste("TT",QT,"TP",PT,".dat",sep="")

		if(filename != "TT200TP375.dat" && filename != "TT200TP450.dat") {
			fit <- read.table(paste(directory,filename,sep=""))

			T <- PT+273.15

			a <- 0.5*(tth2a(fit$V8, 1, 1, 1, 1.033) + tth2a(fit$V20, 2, 0, 0, 1.033))
			a0 <- (1+D_gamma0)*a/(1+D_gamma(T))
			wpC <- a2C(a0)
			wpC <- (wpC - wpC[1])#/(wpC[257] - wpC[1])
			

			points(3.5*fit$V2[1:257], wpC[1:257], type="l", lty=j, col=i, lwd=2)
		}
		j <- j + 1
	}

	i <- i + 1
}