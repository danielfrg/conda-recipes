PWD := $(shell pwd)

all: installer parcel

setup:
	conda install -y openjdk maven; git clone https://github.com/cloudera/cm_ext.git ; cd cm_ext; mvn install
.PHONY: setup

installer:
	constructor .
.PHONY: installer

parcel:
	python build.py *.sh
.PHONY: parcel

validate:
	java -jar cm_ext/validator/target/validator.jar -f output/Anaconda*
.PHONY: validate

manifest:
	python manifest.py
.PHONY: manifest

clean:
	rm -rf output tmp *.sh
.PHONY: clean

cleanall:
	rm -rf cm_ext output tmp *.sh
.PHONY: cleanall
