NAME := hyperconda
VERSION := 1.0.0
OS_VERSION := el6
WORKDIR := ./tmp
OUTPUTDIR := ./output
INSTALLER := miniconda.sh
INSTALLER_URL := https://repo.continuum.io/miniconda/Miniconda3-4.3.21-Linux-x86_64.sh

all: installer parcel manifest

setup:
	conda install -y openjdk maven; git clone https://github.com/cloudera/cm_ext.git ; cd cm_ext; mvn install
.PHONY: setup

installer:
	bash installer.sh
.PHONY: installer

parcel:
	bash parcel.sh
.PHONY: parcel

manifest:
	python manifest.py $(NAME) $(VERSION) $(OS_VERSION) $(OUTPUTDIR)
.PHONY: manifest

validate:
	java -jar cm_ext/validator/target/validator.jar -f output/*.parcel
.PHONY: validate

clean:
	rm -rf output tmp $(INSTALLER)
.PHONY: clean

cleanall:
	rm -rf cm_ext output tmp $(INSTALLER)
.PHONY: cleanall
