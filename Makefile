.PHONY: clean-testing
clean-testing:
	rm -Rf ~/.apkg@agda-2.5.4/ && rm -Rf .agda

# python -m unittest tests/basic.py

.PHONY : clean
clean:
	- rm -Rf agda_pkg.egg-info

.PHONY : test
test:
	- @echo "=================================================="
	- apkg clean
	- apkg init
	- rm -Rf /tmp/agda-stdlib
	- cd /tmp/ && git clone http://github.com/agda/agda-stdlib
	- rm -Rf /tmp/agda-prop
	- cd /tmp/ && git clone http://github.com/jonaprieto/agda-prop
	- rm -Rf /tmp/agda-metis
	- cd /tmp/ && git clone http://github.com/jonaprieto/agda-metis
	- @echo "=================================================="
	- cd /tmp/agda-stdlib && apkg install --no-dependencies
	- cd /tmp/agda-prop && apkg install --no-dependencies
	- cd /tmp/agda-metis && apkg install --no-dependencies
	- cd /tmp/agda-metis && make test 
	- @echo "=================================================="
	- apkg --help
	- apkg
	- @echo "=================================================="
	- apkg list
	- apkg list --short
	- @echo "=================================================="
	- apkg update fotc
	- apkg freeze
	- @echo "=================================================="
	- apkg search agda
	- apkg info agda-prop
	- apkg freeze
	- @echo "=================================================="
	- apkg uninstall agda-metis --yes --remove-cache
	- apkg freeze
	- @echo "=================================================="
	- apkg clean
	- apkg init
	- apkg install --github agda/agda-stdlib --version v0.16
	- apkg install agda-prop
	- apkg install --git http://github.com/jonaprieto/agda-metis.git
	- @echo "=================================================="
	- cd /tmp/agda-metis && make test
	- @echo "=================================================="
	- apkg clean
	- apkg init
	- apkg install agda-metis

	- cd /tmp/agda-metis && make test

.PHONY : TODO
TODO :
	@find src -type d \( -path './.git' -o -path './dist' -o -path './build' -o -path './venv' \) -prune -o -print \
	| xargs grep -I 'TODO' \
	| sort

.PHONY: pip-package
pip-package:
	rm -Rf dist
	rm -Rf build
	python setup.py build
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*

# pip install twine

.PHONY : deploy
deploy :
	$(eval VERSION := $(shell bash -c 'read -p "Version: " pwd; echo $$pwd'))
	echo
	$(eval MSG := $(shell bash -c 'read -p "Comment: " pwd; echo $$pwd'))
	git add .
	git tag v$(VERSION)
	git commit -am "[ v$(VERSION) ] $(MSG)"
	make pip-package
	git push origin master --tags

.PHONY : downloads
downloads:
	pypinfo agda-pkg country
	pypinfo agda-pkg
	pypinfo agda-pkg version
