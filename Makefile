prefix ?= $(HOME)
docdir ?= $(prefix)/share/doc/mockfs/html
webdir ?= $(docdir)

NOSE ?= nosetests
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
	@mkdir -p $(DESTDIR)$(docdir)
	@$(RSYNC) docs/build/html/ $(DESTDIR)$(docdir)/

website-docs: docs
	@mkdir -p $(DESTDIR)$(webdir)
	@$(RSYNC) docs/build/html/ $(DESTDIR)$(webdir)/

test: all
	@$(MAKE) -C docs doctest
	@$(NOSE) --with-doctest

.PHONY: all docs install install-docs website-docs test
