prefix ?= $(HOME)
docdir ?= $(DESTDIR)$(prefix)/share/doc/mockfs/html
webdir ?= $(docdir)
PYTHON ?= python
RSYNC ?= rsync -r --stats --delete --exclude=.gitignore --exclude=.git
RM ?= rm

# Site configuration goes in untracked config.mak
-include config.mak

all: mockfs/*.py setup.py
	$(PYTHON) setup.py build

install: all
	$(PYTHON) setup.py install --prefix=$(DESTDIR)$(prefix)

docs: all
	@$(RM) -rf docs/build
	@$(MAKE) -C docs html

install-doc: docs
	@$(RSYNC) docs/build/html/ $(docdir)/

website-docs: docs
	@$(RSYNC) docs/build/html/ $(webdir)/

test: all
	@make -C docs doctest
	@nosetests --with-doctest

.PHONY: all docs install install-docs website-docs test
