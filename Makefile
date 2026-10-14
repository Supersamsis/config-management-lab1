.PHONY: run test lint clean

run:
	py -3.11 -m src.main

test:
	py -3.11 -m pytest tests/ -v

lint:
	py -3.11 -m flake8 src/ tests/

clean:
	rm -rf __pycache__ .pytest_cache