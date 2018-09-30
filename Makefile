.PHONY: clean-testing
clean-testing:
	rm -Rf ~/.apkg@agda-2.5.4/ && rm -Rf .agda

# python -m unittest tests/basic.py

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
