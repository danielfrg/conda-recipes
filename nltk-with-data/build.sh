#!/bin/bash

python setup.py install --single-version-externally-managed --record=record.txt

NTLK_DATA=$PREFIX/share/nltk_data

# Download data option 1:
# python -m nltk.downloader -d $NTLK_DATA all

# Download data option 2: Direct download and extract each file
mkdir -vp $NTLK_DATA
curl -L -O https://github.com/nltk/nltk_data/archive/gh-pages.zip
unzip gh-pages.zip
mv nltk_data-gh-pages/packages/* $NTLK_DATA
find $NTLK_DATA/ -name "*.zip" | while read filename; do unzip -o -d "`dirname "$filename"`" "$filename"; done;
find $NTLK_DATA/ -name "*.gz" | while read filename; do gunzip -k "$filename"; done;

# Remove original zip files
find $NTLK_DATA/ -name "*.zip" -delete
find $NTLK_DATA/ -name "*.gz" -delete
