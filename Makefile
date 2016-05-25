zncnoticeslack.pyc: zncnoticeslack.py
	cp zncnoticeslack.py zncnoticeslack.copy.py
	python3 -m compileall zncnoticeslack.copy.py
	cp __pycache__/zncnoticeslack.*.pyc zncnoticeslack.pyc
	rm zncnoticeslack.copy.py

lint: zncnoticeslack.py
	flake8 zncnoticeslack.py

install: zncnoticeslack.pyc
	cp zncnoticeslack.pyc $(HOME)/.znc/modules/zncnoticeslack.pyc

clean:
	-rm -rf zncnoticeslack.so zncnoticeslack.pyc __pycache__

