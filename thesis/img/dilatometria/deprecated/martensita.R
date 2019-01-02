var <- read.table("~/Dropbox/Dilatometria/2014-05-19/1_fofo-880oC30min-until-100oC_05.19.14.asc")

png("martensita.png",width=2000,height=1800,res=400)
par(mar=c(3,3,0,0))
plot(V3~V4,data=var[seq(1,length(var$V3),10),],type="b",cex=.5,xlab="",ylab="")
mtext("Temperatura [°C]", side=1, line=2)
mtext("Dilatação relativa [%]", side=2, line=2)
dev.off()

png("martensita2.png",width=2000,height=1800,res=400)
par(mar=c(3,3,0,0))
plot(V3~V4,data=var[seq(3000,length(var$V3),10),],type="p",ylim=c(-0.5,0.5),xlim=c(-100,400),xlab="",ylab="")
mtext("Temperatura [°C]", side=1, line=2)
mtext("Dilatação relativa [%]", side=2, line=2)
dev.off()


alpha <- function(T) {
	return(0.17501+9.51282e-4*T)
}
gamma <- function(T) {
	return(-0.59841+0.00187*T)
}

KM <- function(T) {
	return(exp(-0.01235*(221.069-T)))
}

T <- 0
dil <- 0
f_g <- 0
for(j in 3762:length(var$V4)) {
	T <- c(T,var$V4[j])
	dil <- c(dil,var$V3[j])
	#calcula a fração volumétrica de austenita
	f_g <- c(f_g,(alpha(var$V4[j])-var$V3[j])/(alpha(var$V4[j])-gamma(var$V4[j])))
}

T <- T[-1]
dil <- dil[-1]
f_g <- f_g[-1]

png("frac_martensita.png",width=2000,height=1800,res=400)
par(mar=c(3,4,0,0))
plot(f_g[seq(1,length(T),10)]~T[seq(1,length(T),10)],type="p",xlim=c(-100,250),xlab="",ylab="")
mtext("Temperatura [°C]", side=1, line=2)
mtext(expression(paste("Fração não transformada de austenita ", (f^gamma))), side=2, line=2)
points(KM(T)~T,type="l",col=2)

KM_eq <- expression(paste(f^gamma==exp,"[",-1,",",23%*%10^-2,"(",221,",",1-TT,")]"))
legend("topleft", c("Dados experimentais","Equação ajustada:", KM_eq),lty=c(-1,1,-1),col=c(1,2,-1),pch=c(1,-1,-1),bty="n")
dev.off()

