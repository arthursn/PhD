#!/usr/bin/env Rscript

lag <- 4

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
setPT <- c(200,250,300,375,450)

#filename <- "f_isothermal.png"
#png(paste("~/Desktop/",filename,sep=""), width=2000, height=2000,res=300)
icritico <- rep(0,length(setQT)*length(setPT))

i <- 1
for (PT in setPT) {
	filename <- paste("f_isoPT",PT,".png",sep="")
	png(filename, width=2000, height=2000,res=450)

	par(mar=c(3,3.2,0,0))
	plot(c(0,1),c(0,1),xlim=c(0,900),ylim=c(0,1),type="n",xlab="",ylab="")
	grid()
	mtext("Tempo de partição [s]", side=1, line=2)
	mtext(expression(f^{alpha*"-iso"}==f^{alpha}-f^{alpha*"'"}), side=2, line=2)

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

			total <- sum_g + sum_a

			f_a <- sum_a/total

			kcritico <- length(f_a)
			for(k in 2:length(f_a)) {
				if(abs(f_a[k]-f_a[k-1]) > 0.1) {
					kcritico <- k-1
					break
				}
			}
			f_aiso <- f_a - f_a[1]
			points(3.5*fit$V2[seq(1,kcritico,lag)], f_aiso[seq(1,kcritico,lag)], type="l", lty=j)
			#points(3.5*fit$V2[seq(1,kcritico,lag)], f_aiso[seq(1,kcritico,lag)], type="p", pch=j, cex=.8)

			write.table(file=paste("data/f_a",filename,sep=""), cbind(3.5*fit$V2, f_a, f_aiso), col.names=FALSE, row.names=FALSE)

			if(kcritico < length(f_a)) {
				points(3.5*fit$V2[(kcritico+1):length(f_a)], rep(1-f_a[1],length(f_a)-kcritico), type="l", lty=j)
			}

			icritico[(i-1)*3+j] <- kcritico
		}

		j <- j + 1
	}

	legend("topleft", paste("TT=", setQT, "°C & TP=", PT, "°C", sep=""), bty="n",lty=1:length(setQT))
	graphics.off()

	########################################################################################

	filename <- paste("wC_gamma",PT,".png",sep="")
	png(filename, width=2000, height=2000,res=450)

	par(mar=c(3,3.2,0,0))
	plot(c(0,1),c(0,1),xlim=c(0,900),ylim=c(0,1),type="n",xlab="",ylab="")
	grid()
	mtext("Tempo de partição [s]", side=1, line=2)
	mtext(expression(paste(Delta,"%",w[C]^gamma)), side=2, line=2)
	j <- 1
	for (QT in setQT){
		filename <- paste("TT",QT,"TP",PT,".dat",sep="")

		if(filename != "TT200TP375.dat" && filename != "TT200TP450.dat") {
			fit <- read.table(paste(directory,filename,sep=""))

			T <- PT+273.15

			a <- tth2a(fit$V8, 1, 1, 1, 1.033)
			a0 <- (1+D_gamma0)*a/(1+D_gamma(T))
			#wpC <- cbind(wpC,a2C(a0))
			wpC <- a2C(a0)
			wpC <- wpC - wpC[1]
			
			kcritico <- icritico[(i-1)*3+j]

			points(3.5*fit$V2[seq(1,kcritico,lag)], wpC[seq(1,kcritico,lag)], type="l", lty=j)
			#points(3.5*fit$V2[seq(1,kcritico,lag)], wpC[seq(1,kcritico,lag)], type="p", pch=j, cex=.8)
			wpC[kcritico:length(wpC)] <- 0
			
			write.table(file=paste("data/wC",filename,sep=""), cbind(3.5*fit$V2, wpC), col.names=FALSE, row.names=FALSE)
		}
		j <- j + 1
	}
	if(PT == 450) {
		legend("topleft", paste("TT=", c(140,170), "°C & TP=", PT, "°C", sep=""), bty="n",lty=1:2)
	} else {
		legend("topleft", paste("TT=", setQT, "°C & TP=", PT, "°C", sep=""), bty="n",lty=1:3)
	}	
	graphics.off()

	i <- i + 1
}


x <- seq(28,35,.01)
y <- rep(0,length(x))

i <- 153

fit <- read.table("fitted/TT140TP450.dat")
attach(fit)
y <- V9[i]*exp(-((x-V8[i])/V10[i])**2) + V13[i]*exp(-((x-V12[i])/V14[i])**2) + V17[i]*exp(-((x-V16[i])/V18[i])**2) + V21[i]*exp(-((x-V20[i])/V22[i])**2)
detach(fit)

#plot(x,y,type="l")
