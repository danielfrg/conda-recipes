#!/bin/bash

NAME=hyperconda
VERSION=1.0.0
SUFFIX=el6
WORKDIR=./tmp
OUTPUTDIR=./output

echo "Patching installation ..."
# $WORKDIR/bin/python patch.py $WORKDIR

echo "Writing metadata ..."
# $WORKDIR/bin/python metadata.py $NAME $VERSION $SUFFIX $WORKDIR

echo "Writing parcel ..."
mkdir -vp $OUTPUTDIR
cd $WORKDIR && tar czf ../$OUTPUTDIR/$NAME-$VERSION-$SUFFIX.parcel .
