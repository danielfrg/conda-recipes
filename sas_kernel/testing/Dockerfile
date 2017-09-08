FROM continuumio/miniconda3:4.3.14

RUN apt-get install -y ssh

RUN conda config --add channels conda-forge
RUN conda install -y jupyter notebook jupyterlab
RUN conda install -y -c danielfrg sas_kernel

RUN mkdir /work
WORKDIR /work

ADD cmd.sh /bin/cmd.sh
RUN chmod +x /bin/cmd.sh
CMD ["/bin/cmd.sh"]
