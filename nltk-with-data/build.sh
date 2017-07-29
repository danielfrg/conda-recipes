#!/bin/bash

python setup.py install --single-version-externally-managed --record=record.txt

# Download data
python -m nltk.downloader -d $PREFIX/nltk_data all
# Remove original zip files
rm $PREFIX/nltk_data/**/*.zip
