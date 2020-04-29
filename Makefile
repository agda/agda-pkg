.PHONY: clean-testing
clean-testing:
	rm -Rf ~/.apkg@* && rm -Rf .agda

# python -m unittest tests/basic.py

.PHONY : clean
clean:
	- rm -Rf agda_pkg.egg-info



# Silly testing

.PHONY : test
test:
	@echo   "T.help ++++++++++++++++++++++++++++++++++++++++++++++++++++"
	@apkg --help \
	&& echo "T.version +++++++++++++++++++++++++++++++++++++++++++++++++" \
	&& apkg --version \
	&& echo "T.- ++++++++++++++++++++++++++++++++++++++++++++++++++++++" \
	&& apkg \
	&& echo "T.clean +++++++++++++++++++++++++++++++++++++++++++++++++++" \
	&& apkg clean --yes \
	&& echo "T.init ++++++++++++++++++++++++++++++++++++++++++++++++++++" \
	&& apkg init \
	&& echo "T.list ++++++++++++++++++++++++++++++++++++++++++++++++++++" \
	&& apkg list \
	&& echo "T.list --field name +++++++++++++++++++++++++++++++++++++++" \
	&& apkg list --field name \
	&& echo "T.list --field url ++++++++++++++++++++++++++++++++++++++++" \
	&& apkg list --field url \
	&& echo "T.list --field version ++++++++++++++++++++++++++++++++++++" \
	&& apkg list --field version \
	&& echo "T.upgrade +++++++++++++++++++++++++++++++++++++++++++++++++" \
	&& apkg upgrade  \
	&& echo "T.freeze (nothing)+++++++++++++++++++++++++++++++++++++++++" \
	&& apkg freeze	\
	&& echo "T.search +++++++++++++++++++++++++++++++++++++++++++++++++" \
	&& apkg search standard  \
	&& echo "T.install ++++++++++++++++++++++++++++++++++++++++++++++++" \
	&& apkg install standard-library --version v1.1 \
	&& echo "T.freeze +++++++++++++++++++++++++++++++++++++++++++++++++" \
	&& apkg freeze


.PHONY : test-install-github
test-install-github:
	@echo "++++++++++++++++++++++++++++++++++++++++++++++++" \
	&& apkg clean  \
	&& apkg init  \
	&& apkg install --github jonaprieto/agda-prop \
	&& apkg install --github agda/agda-stdlib --version v0.16 \
	&& apkg install --git http://github.com/jonaprieto/agda-metis.git
	&& apkg freeze


.PHONY : test-local
test-local:
	@echo "++++++++++++++++++++++++++++++++++++++++++++++++" \
	&& apkg clean \
	&& apkg init \
	&& rm -Rf /tmp/agda-stdlib \
	&& cd /tmp/ && git clone http://github.com/agda/agda-stdlib \
	&& rm -Rf /tmp/agda-prop \
	&& cd /tmp/ && git clone http://github.com/jonaprieto/agda-prop \
	&& rm -Rf /tmp/agda-metis \
	&& cd /tmp/ && git clone http://github.com/jonaprieto/agda-metis \
	&& echo "++++++++++++++++++++++++++++++++++++++++++++++++" \
	&& cd /tmp/agda-stdlib && apkg install --no-dependencies \
	&& cd /tmp/agda-prop && apkg install --no-dependencies \
	&& cd /tmp/agda-metis && apkg install --no-dependencies \
	&& cd /tmp/agda-metis && make test
	&& apkg freeze


.PHONY : test-local-with-dependencies
test-local-with-dependencies:
	@echo   "++++++++++++++++++++++++++++++++++++++++++++++++" \
	&& apkg clean \
	&& apkg init \
	&& rm -Rf /tmp/agda-metis \
	&& cd /tmp/ && git clone http://github.com/jonaprieto/agda-metis \
	&& echo "++++++++++++++++++++++++++++++++++++++++++++++++" \
	&& cd /tmp/agda-metis && apkg install \
	&& cd /tmp/agda-metis && make test \
	&& apkg freeze


.PHONY : all-tests
all-tests:
	   make test 
	&& make test-local
	&& make test-local-with-dependencies
	&& make test-install-github

.PHONY : TODO
TODO :
	@find agda-pkg -type d \( -path './.git' -o -path './dist' -o -path './build' -o -path './venv' \) -prune -o -print \
	| xargs grep -I 'TODO' \
	| sort

.PHONY: pip-package
pip-package:
	rm -Rf dist
	rm -Rf build
	python3 setup.py build
	python3 setup.py sdist
	python3 setup.py bdist_wheel --universal
	twine upload dist/*

# pip install twine
# $(eval VERSION := $(shell bash -c 'read -p "Version: " pwd; echo $$pwd'))

.PHONY : deploy
deploy :
	@python3 deploy.py


.PHONY: push
push:
	make pip-package 
	git push origin master --tags
	
.PHONY : downloads
downloads:
	pypinfo agda-pkg country
	pypinfo agda-pkg version
	pypinfo agda-pkg
