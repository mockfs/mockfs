CTAGS ?= ctags
NOSE ?= nosetests
PYTHON ?= python
RSYNC ?= rsync -r --stats --delete --exclude=.gitignore --exclude=.git
RM ?= rm

# Define MOCKFS_PREFIX in the environment to override the default prefix,
# or supply "DESTDIR" and "prefix" on the command-line, e.g.
#     make DESTDIR=/tmp/DESTDIR prefix=/usr install

MOCKFS_PREFIX ?= $(CURDIR)/mockfs-$(version)

prefix ?= $(MOCKFS_PREFIX)
libdir ?= $(shell $(PYTHON) -c 'import os, distutils.sysconfig as sc; print(os.path.basename(sc.get_config_var("LIBDIR")))')
pythonver ?= $(shell $(PYTHON) -c 'import distutils.sysconfig as sc; print(sc.get_python_version())')
pythonsite ?= $(prefix)/$(libdir)/python$(pythonver)/site-packages
docdir ?= $(prefix)/share/doc/mockfs/html
webdir ?= $(docdir)
version ?= $(shell grep __version__ mockfs/__init__.py | \
		awk '{print $$3}' | sed -e "s,',,g")

SETUP_INSTALL_ARGS ?= --single-version-externally-managed --record MANIFEST
ifdef DESTDIR
    SETUP_INSTALL_ARGS += --root=$(DESTDIR)
endif
ifndef mac_pkg
    SETUP_INSTALL_ARGS += --prefix=$(prefix)
    SETUP_INSTALL_ARGS += --install-lib=$(pythonsite)
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
