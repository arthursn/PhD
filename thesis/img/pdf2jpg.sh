#!/bin/bash

#mogrify -format jpg *.tif
#mogrify -crop 2048x1760+0+0 *.jpg
#
#for file in *.jpg;
#do
	#prefix=${file%-*}
	#echo $file;
	#convert $file -gravity SouthEast ../../$prefix.jpg -compose Over -composite $file;
#done
#

for file in *.pdf;
do
	prefix=${file%.*}
	echo $file;
	#convert -format jpg $file $prefix.jpg;
	convert  -verbose -density 150 -trim $file -quality 100 -sharpen 0x1.0 $prefix.jpg
done


