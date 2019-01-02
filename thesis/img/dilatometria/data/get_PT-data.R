############################ Têmpera e Partição

iso.inc <- c(999, 999, 999,
			 999, 999, 999,
			 999, 999, 999)
iso.s <- c(4888, 4770, 4667,
		   4707, 4594, 4481,
		   4608, 4495, 4382)
iso.f <- iso.s + iso.inc

files <- c("140-375.asc", "170-375.asc", "200-375.asc",
		   "140-300.asc", "170-300.asc", "200-300.asc",
		   "140-250.asc", "170-250.asc", "200-250.asc")

files.PT <- gsub(".asc", "-PT.asc", files)
files.PT <- paste("PT",files.PT,sep="/")

for (j in 1:length(files)) {
	data <- read.table(files[j], col.names=c("index", "time.s", "dl.pct", "TC1"))
	data.PT <- data[iso.s[j]:iso.f[j],]

	data.PT$time.s <- data.PT$time.s - data.PT$time.s[1]
	data.PT$dl.pct <- data.PT$dl.pct - data.PT$dl.pct[1]

	write.table(file=files.PT[j], x=data.PT, row.names=FALSE)
}

############################ Têmpera e Partição outra disposição dos eixos

iso.inc <- c(999)
iso.s <- c(4617)
iso.f <- iso.s + iso.inc

files <- c("170-300_heating50oCs-1.asc")

files.PT <- gsub(".asc", "-PT.asc", files)
files.PT <- paste("PT",files.PT,sep="/")

for (j in 1:length(files)) {
	data <- read.table(files[j], col.names=c("index", "time.s", "TC1", "dl.um", "T.n"))

	data.PT <- data[iso.s[j]:iso.f[j],]

	data.PT$time.s <- data.PT$time.s - data.PT$time.s[1]
	data.PT$dl.pct <- (data.PT$dl.um - data.PT$dl.um[1])*100/10e3

	write.table(file=files.PT[j], x=data.PT, row.names=FALSE)
}

############################ Austempera

iso.inc <- c(999, 999, 999, 999, 999)
iso.s <- c(3993, 3897, 3805, 3695, 3556) #determinado visualmente pelo gnuplot
iso.f <- iso.s + iso.inc

files <- c("200.asc", "250.asc", "300.asc", "375.asc", "450.asc")

files.PT <- paste("austempera",files,sep="/")

for (j in 1:length(files)) {
	data <- read.table(files[j], col.names=c("index", "time.s", "dl.pct", "TC1"))
	data.PT <- data[iso.s[j]:iso.f[j],]

	data.PT$time.s <- data.PT$time.s - data.PT$time.s[1]
	data.PT$dl.pct <- data.PT$dl.pct - data.PT$dl.pct[1]

	write.table(file=files.PT[j], x=data.PT, row.names=FALSE)
}