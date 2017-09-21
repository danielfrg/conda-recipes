PWD := $(shell pwd)

docker-image:
	docker build -t conda-build .
.PHONY: docker-image

docker-run:
	docker run -it -v $(PWD):/root/staged-recipes -v $(PWD)/cache/conda-bld:/conda-bld -v $(PWD)/cache/maven:/root/.m2 conda-build
.PHONY: docker-run

clean:
	rm -rf cache/conda-bld
.PHONY: clean

cleanall:
	rm -rf cache
.PHONY: cleanall
