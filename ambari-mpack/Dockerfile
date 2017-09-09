FROM debian:jessie

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1

RUN wget --quiet https://repo.continuum.io/miniconda/Miniconda3-4.2.12-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh

ENV PATH=/opt/conda/bin:$PATH

ADD environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml

ENV PATH=/opt/conda/envs/anaconda-ambari/bin:$PATH

VOLUME /ambari-extensions
WORKDIR /ambari-extensions
