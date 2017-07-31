PWD := $(shell pwd)

docker-image:
	docker build -t conda-build .
.PHONY: docker-image

docker-run:
	docker run -it -v $(PWD):/work -v $(PWD)/conda-bld:/conda-bld -v $(PWD)/cache/maven:/root/.m2 conda-build
.PHONY: docker-run
