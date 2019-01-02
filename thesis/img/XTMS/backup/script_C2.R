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

#a <- function(xC, T) {
#	val <- 10*(0.363067 + 0.000783*xC)*(1+(24.92-0.51*xC)*1e-6*(T-1000))
#	return(val)
#}

#Newton <- function(a0, T){
#	T <- T + 273.15
#	h <- 1e-4
#	x <- 0.1
#	for (i in 1:10) {
#		derivative <- (a(x+h,T) - a(x-h,T))/(2*h)
#		x <- x - (a(x,T)-a0)/derivative
#		print(x)
#	}
#	return(x)
#}

f0 <- f_gamma(300)
index <- c(52,53.1,54,55,56,57,58,59,60)
PT <- c(200,250,300,200,250,300,200,250,300)
#index <- c(54,57,60)
#T <- c(300,300,300)
T <- PT + 273.15

filename <- "57-wtC.png"
png(paste("~/Desktop/",filename,sep=""), width=2000, height=2000,res=300, bg="#ffffff00")
plot(c(0,1),c(0,1),xlim=c(0,896),ylim=c(0,2),type="n", xlab="Time [s]", ylab="%wt C")

#j<-6
for (j in c(1:5,7:length(index)))
{
	directory <- "~/Documents/XTMS-Gleeble/fofo/fitted/"

	fit <- read.table(paste(directory,index[j],".dat",sep=""))
	fit$V2 <- (fit$V2-1)*3.5

	a <- tth2a(fit$V8, 1, 1, 1, 1.036)
	a0 <- (1+f0)*a/(1+f_gamma(T[j]))
	wpC <- a2C(a0)

	#print(wpC)

	points(wpC~fit$V2, type="l", lty=ceiling(j/3), col=((j-1)%%3+1))
}

legend("topleft", paste("QT=", rep(c(140,170,200),3), "°C & PT=", rep(c(200,250,300),each=3), "°C", sep=""), col=rep(1:3,each=3), lty=rep(1:3,3))
dev.off()