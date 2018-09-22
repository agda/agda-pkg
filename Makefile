.PHONY: clean-testing
clean-testing:
	rm -Rf ~/.apkg@agda-2.5.4/ && rm -Rf .agda

.PHONY : test
test:
	python -m unittest tests/basic.py