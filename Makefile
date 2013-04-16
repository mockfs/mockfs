version ?= $(shell grep __version__ mockfs/__init__.py | \
		awk '{print $$3}' | sed -e "s,',,g")
prefix ?= $(CURDIR)/mockfs-$(version)
docdir ?= $(prefix)/share/doc/mockfs/html
webdir ?= $(docdir)

CTAGS ?= ctags
NOSE ?= nosetests
PYTHON ?= python
RSYNC ?= rsync -r --stats --delete --exclude=.gitignore --exclude=.git
RM ?= rm

SETUP_INSTALL_ARGS = --single-version-externally-managed --record MANIFEST
ifdef DESTDIR
    SETUP_INSTALL_ARGS += --root=$(DESTDIR)
endif
ifndef mac_pkg
    SETUP_INSTALL_ARGS += --prefix=$(prefix)
endif

# Site configuration goes in untracked config.mak
-include config.mak

all: mockfs/*.py setup.py
	@echo mockfs v$(version)
	$(PYTHON) setup.py build

install: all
	$(PYTHON) setup.py install $(SETUP_INSTALL_ARGS)

docs: all
	@$(RM) -rf docs/build
	@$(MAKE) -C docs html

install-doc: docs
	@mkdir -p $(DESTDIR)$(docdir)
	@$(RSYNC) docs/build/html/ $(DESTDIR)$(docdir)/

website-docs: docs
	@mkdir -p $(DESTDIR)$(webdir)
	@$(RSYNC) docs/build/html/ $(DESTDIR)$(webdir)/

tags:
	find mockfs -name '*.py' -print0 | xargs -0 $(CTAGS)

test: all
	@$(MAKE) -C docs doctest
	@$(NOSE) --with-doctest

.PHONY: all docs install install-docs website-docs tags test
