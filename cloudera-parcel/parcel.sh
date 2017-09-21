#!/bin/bash

NAME=hyperconda
VERSION=1.0.0
OS_VERSION=el6
WORKDIR=./tmp
OUTPUTDIR=./output
PREFIX=$WORKDIR/$NAME-$VERSION

echo "Patching installation ..."
$PREFIX/bin/python patch.py $PREFIX

echo "Writing metadata ..."
$PREFIX/bin/python metadata.py $NAME $VERSION $OS_VERSION $PREFIX

echo "Writing parcel ..."
mkdir -vp $OUTPUTDIR
cd $WORKDIR && tar czf ../$OUTPUTDIR/$NAME-$VERSION-$OS_VERSION.parcel $NAME-$VERSION
