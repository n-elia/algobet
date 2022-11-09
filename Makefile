.PHONY: test
test:
	PYTHONPATH=./src pytest src/test/ --html=src/test/reports/pytest_report.html -c src/test/conftest.py --sandbox
