.PHONY: run debug test install clean build
run:
	cd src && python3 -m keyboard

test:
	python3 -m unittest discover -s src

install:
	python3 -m pip install .

install_updatable:
	python3 -m pip install git+git://github.com/larkwt96/keyboard.git
