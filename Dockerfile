FROM continuumio/miniconda3:4.3.14

RUN conda install -y conda-build anaconda-client constructor certifi
RUN conda config --add channels conda-forge

WORKDIR /work
