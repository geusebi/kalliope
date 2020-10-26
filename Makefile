.PHONY: tests

all: 
	

tests:
	python3 -m unittest -v tests

clean:
	rm -rf __pycache__
	rm -rf pykalliope/__pycache__
	rm -rf tests/__pycache__

