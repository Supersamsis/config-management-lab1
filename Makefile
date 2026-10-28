.PHONY: run test clean

run:
	py -3.11 -m src.main

test:
	py -3.11 -m pytest tests/ -v

clean:
	py -3.11 -c "import shutil; shutil.rmtree('__pycache__', ignore_errors=True); shutil.rmtree('.pytest_cache', ignore_errors=True)"