BLACK ?= black
CTAGS ?= ctags
PYTHON ?= python
PYTEST ?= $(PYTHON) -m pytest
RSYNC ?= rsync -r --stats --delete --exclude=.gitignore --exclude=.git
RM ?= rm
TOX ?= tox

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

BLACK_ENABLED := $(shell sh -c 'type black >/dev/null 2>&1 && echo 1 || echo 0')

# Site configuration goes in untracked config.mak
-include config.mak

all:: mockfs/*.py setup.py
	@echo mockfs v$(version)
	$(PYTHON) setup.py build

install: all
	$(PYTHON) setup.py install $(SETUP_INSTALL_ARGS)

tags:
	find mockfs -name '*.py' -print0 | xargs -0 $(CTAGS)

test: all
	$(PYTEST)

tox:
	$(TOX) --skip-missing-interpreters -e 'py{27,36,37,38}'

format::
ifeq ($(BLACK_ENABLED),1)
	$(SILENT)git ls-files -z -- '*.py' \
	| xargs -0 black --skip-string-normalization --target-version py27
endif

.PHONY: all install tags test
