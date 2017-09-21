#!/bin/bash

NAME=hyperconda
VERSION=1.0.0
INSTALLER=miniconda.sh
INSTALLER_URL=https://repo.continuum.io/miniconda/Miniconda3-4.3.21-Linux-x86_64.sh
WORKDIR=./tmp
PREFIX=$WORKDIR/$NAME-$VERSION

if [ ! -f $INSTALLER ]; then
    echo "Downloading $INSTALLER ..."
    curl -s -o $INSTALLER $INSTALLER_URL
fi

echo "Extracting installer ..."
rm -rf $WORKDIR
bash $INSTALLER -b -p $PREFIX

echo "Installing packages ..."
$PREFIX/bin/conda env update .

echo "Cleaning installation ..."
$PREFIX/bin/conda clean --yes --all
