PWD := $(shell pwd)

docker-image:
	docker build -t conda-build .
.PHONY: docker-image

docker-run:
	docker run -it -v $(PWD):/work -v $(PWD)/conda-bld:/opt/conda/conda-bld -v $(PWD)/cache/m2://.m2 conda-build
.PHONY: docker-run
