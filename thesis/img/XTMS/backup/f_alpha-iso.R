#!/usr/bin/env Rscript

lag <- 1

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
setPT <- c(250,300,375,450)

icritico <- rep(0,length(setQT)*length(setPT))


plot(c(0,1),c(0,1),xlim=c(0,900),ylim=c(0,1),type="n",xlab="",ylab="")

Ta <- 880

i <- 1
for (PT in setPT) {
	if(PT == 375) {
		setQT <- c(140,170)
	} else if(PT == 450) {
		setQT <- c(140,170)
	} else {
		setQT <- c(140,170,200)
	}

	j <- 1
	for (QT in setQT){
		filename <- paste("TT",QT,"TP",PT,".dat",sep="")

		if(filename != "TT200TP375.dat" && filename != "TT200TP450.dat") {
			fit <- read.table(paste(directory,filename,sep=""))

			pg111 <- abs(fit$V9*fit$V10)/g111
			pa110 <- abs(fit$V13*fit$V14)/a110+abs(fit$V17*fit$V18)/a110-abs(fit$V17[1]*fit$V18[1])/a110
			pg200 <- abs(fit$V21*fit$V22)/g200
			
			sum_g <- (pg111+pg200)/2
			sum_a <- pa110
			sum_a <- sum_a# - sum_a[1]

			total <- sum_g + sum_a

			f_a <- sum_a/total
			f_g <- sum_g/total

			kcritico <- length(f_a)
			for(k in 2:length(f_a)) {
				if(abs(f_a[k]-f_a[k-1]) > 0.05) {
					kcritico <- k-1
					break
				}
			}

			if(PT != 450)
				variation <- f_a[257]-f_a[1]
			else
				variation <- f_g[1]

			f_aiso <- (f_a - f_a[1])/variation

			points(3.5*fit$V2[seq(1,kcritico,lag)], f_aiso[seq(1,kcritico,lag)], type="l", lty=j, col=i, lwd=2)

			if(kcritico < length(f_a)) {
				points(3.5*fit$V2[(kcritico+1):length(f_a)], rep(1-f_a[1],length(f_a)-kcritico), type="l", lty=j, col=i, lwd=2)
			}

			icritico[(i-1)*3+j] <- kcritico
		}

		ti <- Ta/10 + 30*60 + (880-QT)/50 + 60 + (PT-QT)/10
		tf <- ti + 15*60

		filename <- paste(QT,"-",PT,".asc",sep="")

		var <- read.table(paste("../dilatometria/data/",filename,sep=""))

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