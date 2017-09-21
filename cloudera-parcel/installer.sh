#!/bin/bash

INSTALLER=miniconda.sh
INSTALLER_URL=https://repo.continuum.io/miniconda/Miniconda3-4.3.21-Linux-x86_64.sh
WORKDIR=./tmp

if [ ! -f $INSTALLER ]; then
    echo "Downloading $INSTALLER ..."
    curl -s -o $INSTALLER $INSTALLER_URL
fi

echo "Extracting installer ..."
# rm -rf $WORKDIR
# bash $INSTALLER -b -p $WORKDIR

echo "Installing packages ..."
$WORKDIR/bin/conda env update .

echo "Cleaning installation ..."
$WORKDIR/bin/conda clean --yes --all
