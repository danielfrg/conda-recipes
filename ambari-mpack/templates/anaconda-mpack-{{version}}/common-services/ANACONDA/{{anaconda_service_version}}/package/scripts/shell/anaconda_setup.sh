
#!/bin/bash
set -eu

FILES_DIR=$1

bash $FILES_DIR/Anaconda-{{ constructor_version }}-Linux-x86_64.sh -b -p /opt/continuum/anaconda
