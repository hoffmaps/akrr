#!/bin/bash

# input file is argument 1 in this case if it's right after docker argument
HPCCINF=$1 

INFILE="default_hpccinf.txt"

echo "You input the following file: " $HPCCINF

# checks if the given file is not the default file - need to change file name in this case
if [ $HPCCINF != "default" ]
then
	INFILE=$HPCCINF
fi

# goes to the input directory to get file
cd ./inputs

if [ -r $INFILE ]
then
	cp $INFILE ../hpccinf.txt
else
	echo "File does not exist in inputs or does not have read permissions"
fi

cd ..

echo "The file $INFILE is now hpccinf.txt in the same directory as hpcc"
#echo '$0 = ' $0
#echo '$1 = ' $1

pwd

# this allows us to go back into bash (nice for debugging and such)
#/bin/bash
