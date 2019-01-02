Dl_gamma <- function(T) {
	B <- 24.8e-6
	Theta <- 280
	f <- B*T + B*Theta*(exp(-T/Theta)-1)
	return(f*1e4)
}

Dl_alpha <- function(T) {
	L0 <- 103.9e-4
	B <- 18.3e-6
	Theta <- 320
	f <- L0 + B*T + B*Theta*(exp(-T/Theta)-1)
	return(f*1e4)
}

T <- 0:1600

png("dilation_alphagamma.png", width=2000, height=1500, res=400)
par(mar=c(3,3.5,0,0))
plot(T, Dl_gamma(T), xlab="", ylab="", type="l")
points(T, Dl_alpha(T), type="l", lty=2)
mtext("Temperatura [K]", side=1, line=2)
mtext(expression(Delta*L/L[0]%*%10^{-4}), side=2, line=2)
legend("topleft", c("CFC", "CCC"), lty=c(1,2), bty="n")
graphics.off()