#Função que calcula a derivada de primeira ordem y em função de x
#Essa função funciona aplicando regressões lineares de y em x no intervalo (i-lag):(i+lag). O valor do coeficiente angular da reta calculado pela regressão é equivalente à derivada no ponto i.
#As variáveis de entrada x e y devem ser na forma de vetores. lag é um número inteiro que representa o tamanho do intervalo utilizado na regressão.
derivative <- function(x,y,lag) {
	dy.dx <- rep(NA, length(x))

	for(i in (1+lag):(length(x)-lag)) {
		reg <- lm(y[(i-lag):(i+lag)]~x[(i-lag):(i+lag)]) #lm é a função de regressão no R.
		dy.dx[i] <- reg$coefficients[2]
	}

	return(dy.dx)
}

testname <- "1_fofoTupy_10oCmin"
#filename <- paste("1", testname, "10.08.14.asc", sep="_")

filename <- "1_fofoTupy_10oCmin-1_10.28.14.asc"

data <- read.table(filename) #Armazena na variável 'data' os dados do arquivo '1_1070Nb...'
T <- data$V4[3000:(5*880)] #Armazena na variável T (de tempeartura) os valores da quarta coluna ($V4) armazenada na variável 'data'. O intervalo 5401:9700 delimita a etapa de resfriamento do ensaio de dilatometria.
dil <- data$V3[3000:(5*880)] #Armazena na variável dil (de dilatação) os valores da terceira coluna ($V3) armazenada na variável 'data'.

ddil.dT <- derivative(T,dil,10) #Aplica a função derivative nas variáveis dil e T utilizando lag=50. Menores valores de lag fornecem curvas mais ruidosas, mas com melhor resolução. Perceba que lag=50 significa que utilizei um intervalo de 2*50 = 100 pontos para determinar a derivada.

#filename <- paste(testname, "derivative.asc", sep="_")
#write.table(cbind(T,dil,ddil.dT), file=filename, row.names=FALSE) #Salva no arquivo xxxx os valores de T, dil e da derivada ddil.dT

#Subrotina para plotagem dos gráficos
filename <- paste(testname, ".png", sep="")
png(filename, width=1500, height=1200, res=300)
par(mar=c(3,3,0,3))
plot(dil[seq(1,length(T),20)]~T[seq(1,length(T),20)], type="p", xlab="", ylab="")
mtext("Temperatura [°C]", side=1, line=2)
mtext(expression(paste(Delta, "L[", mu, "m]")), side=2, line=2)
par(new="T")
plot(ddil.dT~T, type="l", axes=F, xlab="", ylab="")
axis(4)
mtext("dL/dT", side=4, line=2)
dev.off()


filename <- paste(testname, "_2.png", sep="")
png(filename, width=1200, height=1200, res=300)
par(mar=c(3,3,0,0))
plot(V3[seq(1,length(data$V3),20)]~V4[seq(1,length(data$V3),20)], data=data, type="p", cex=.5, xlab="", ylab="")
mtext("Temperatura [°C]", side=1, line=2)
mtext(expression(paste(Delta, "L[", mu, "m]")), side=2, line=2)
dev.off()


