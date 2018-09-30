.PHONY: clean-testing
clean-testing:
	rm -Rf ~/.apkg@agda-2.5.4/ && rm -Rf .agda

# python -m unittest tests/basic.py

.PHONY : clean
clean:
	- rm -Rf agda_pkg.egg-info

.PHONY : test
test:
	- apkg clean
	- apkg init
	- cd /tmp/ && git clone http://github.com/agda/agda-stdlib
	- cd /tmp/ && git clone http://github.com/jonaprieto/agda-prop
	- cd /tmp/ && git clone http://github.com/jonaprieto/agda-metis
	- cd /tmp/agda-stdlib && apkg install
	- cd /tmp/agda-prop && apkg install
	- cd /tmp/agda-metis && apkg install
	- cd /tmp/agda-metis && make test

	- apkg search agda
	- apkg info agda-prop
	- apkg freeze
	- apkg uninstall agda-metis --yes --remove-cache
	- apkg freeze

	- apkg clean
	- apkg init
	- apkg install --github agda/agda-stdlib.git --version v0.16
	- apkg install agda-prop
	- apkg install --git http://github.com/jonaprieto/agda-metis.git
	- cd /tmp/agda-metis && make test


.PHONY : TODO
TODO :
	find . -type d \( -path './.git' -o -path './dist' \) -prune -o -print \
	| xargs grep -I 'TODO' \
	| sort

.PHONY : README.rst
README.rst :
	pandoc --from=rst --to=rst --output=README.rst README.md

.PHONY : deploy 
deploy : README.rst
	pip install twine
	$(eval VERSION := $(shell bash -c 'read -p "Version: " pwd; echo $$pwd'))
	echo
	$(eval MSG := $(shell bash -c 'read -p "Comment: " pwd; echo $$pwd'))
	make clean
	git tag v$(VERSION)
	git commit -am "[ v$(VERSION) ] new version: $(MSG)"
	python setup.py build
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*
	make clean