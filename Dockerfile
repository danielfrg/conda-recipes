FROM condaforge/linux-anvil

RUN yum install -y make unzip

RUN /opt/conda/bin/conda install -y anaconda-client constructor certifi jinja2
# RUN conda config --add channels conda-forge

ENV CONDA_BLD_PATH /conda-bld

WORKDIR /work
