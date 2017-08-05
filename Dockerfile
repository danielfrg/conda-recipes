FROM continuumio/miniconda3:4.3.14

RUN apt-get update && apt-get install make unzip

RUN conda install -y conda-build anaconda-client constructor certifi
RUN conda config --add channels conda-forge

ENV CONDA_BLD_PATH /conda-bld

WORKDIR /work
