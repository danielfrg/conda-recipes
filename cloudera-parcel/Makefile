NAME := hyperconda
VERSION := 1.0.0
SUFFIX := el6
WORKDIR := ./tmp
OUTPUTDIR := ./output

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
	python manifest.py $(NAME) $(VERSION) $(SUFFIX) $(OUTPUTDIR)
.PHONY: manifest

validate:
	java -jar cm_ext/validator/target/validator.jar -f output/*.parcel
.PHONY: validate

clean:
	rm -rf output tmp
.PHONY: clean

cleanall:
	rm -rf cm_ext output tmp
.PHONY: cleanall
