#SOURCES=

.PHONY : docs tests format
	
all: format

format:
	isort pieces tests
	black pieces tests

tests: 
	pytest --doctest-modules

coverage:
	pytest --cov=pieces tests/

clean:
	make -C docs clean

