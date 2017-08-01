PWD := $(shell pwd)

all: installer parcel

setup:
	conda install -y openjdk maven; git clone https://github.com/cloudera/cm_ext.git ; cd cm_ext; mvn install
.PHONY: setup

installer:
	constructor .
.PHONY: installer

parcel:
	python parcel.py Anaconda*
.PHONY: parcel

validate:
	java -jar cm_ext/validator/target/validator.jar -f output/Anaconda*
.PHONY: validate

clean:
	rm -rf cm_ext output tmp *.sh
