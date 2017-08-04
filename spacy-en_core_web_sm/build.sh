#!/bin/bash

SPACY_PKG_NAME="$(cut -d'-' -f2 <<<$PKG_NAME)"

python setup.py install -q --single-version-externally-managed --record=record.txt

# We need to go into a tmp dir so it doesn't think that we mean the $SPACY_PKG_NAME directory
# we mean the $SPACY_PKG_NAME python library
pushd /tmp
python -m spacy link $SPACY_PKG_NAME en
popd
