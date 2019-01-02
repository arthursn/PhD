#!/bin/sh

bitmap=$(find . | grep '.jpg\|.png')

for file in $bitmap; do
	filename=$(basename $file);
	directory=$(dirname $file);

	newfile=$directory/${filename%.*}.pdf;
	convert $file $newfile;
	echo $newfile;
done