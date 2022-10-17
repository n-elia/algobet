.PHONY: test
test:
	PYTHONPATH=. pytest src/test/ --html=src/test/reports/pytest_report.html -c src/test/conftest.py --sandbox