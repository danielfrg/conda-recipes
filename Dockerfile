FROM condaforge/linux-anvil

RUN yum install -y wget tmux make unzip

RUN /opt/conda/bin/conda update -y conda conda-build
RUN /opt/conda/bin/conda install -y conda-build-all conda-forge-build-setup
RUN /opt/conda/bin/conda install -y anaconda-client constructor certifi jinja2

ENV CONDA_BLD_PATH /conda-bld

RUN mkdir -vp /root/staged-recipes
WORKDIR /root/staged-recipes
