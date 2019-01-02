#aplica a lei de Bragg
tth2a <- function(tth, h, k, l, lambda) {
	fator <- sqrt(h**2 + k**2 + l**2)
	a <- 0.5*lambda*fator/sin(tth*pi/360)
	return(a)
}

f_gamma <- function(T) {
	B <- 24.8e-6
	Theta <- 280
	f <- B*T + B*Theta*(exp(-T/Theta)-1)
	return(f)
}

a2C <- function(a) {
	return((a - 3.572 - 0.00157*2.47 + 0.0012*0.2)/.033)
}

directory <- "fitted/"

setQT <- c(140,170,200)
setPT <- c(200,250,300,375,450)

#filename <- "wtC.png"
#png(paste("~/Desktop/",filename,sep=""), width=2000, height=2000,res=300)
plot(c(0,1),c(0,1),xlim=c(0,900),ylim=c(0,1),type="n", xlab="Time [s]", ylab=expression(paste(Delta,"%wt C")))

wpC <- seq(0,256)*3.5

for (PT in setPT) {
	for (QT in setQT){
		filename <- paste("TT",QT,"TP",PT,".dat",sep="")

		if(filename != "TT200TP375.dat" && filename != "TT200TP450.dat") {
			fit <- read.table(paste(directory,filename,sep=""))

			T <- PT+273.15

			a <- tth2a(fit$V8, 1, 1, 1, 1.033)
			a0 <- (1+f0)*a/(1+f_gamma(T))
			#wpC <- cbind(wpC,a2C(a0))
			wpC <- a2C(a0)
			wpC <- wpC - wpC[1]

			points(fit$V2*3.5, wpC, type="l")
		}
	}
}

#legend("topleft", paste("QT=", rep(c(140,170,200),3), "°C & PT=", rep(c(200,250,300),each=3), "°C", sep=""), col=rep(1:3,each=3), lty=rep(1:3,3))
#graphics.off()