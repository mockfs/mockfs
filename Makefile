# The default target of this Makefile is...
.PHONY: all
all::

# Development
# -----------
# make V=1                      # V=1 increases verbosity
# make test [flags=...]         # run tests; flags=-x fails fast, --ff failed first
# make test V=2                 # run tests; V=2 increases test verbosity
# make fmt                      # run the code formatter

# Installation
# ------------
# "prefix" (and, optionally, "DESTDIR") can be passed on the command-line when installing, e.g.
#     make DESTDIR=/tmp/stage prefix=/usr install
prefix ?= $(CURDIR)/dist/mockfs
# DESTDIR =

# Commands
# --------
# The external commands used by this Makefile are...
CERCIS = cercis
GIT = git
PIP = pip
PYTHON ?= python
PYTEST ?= $(PYTHON) -m pytest
TOX ?= tox
XARGS = xargs

# Flags and Control Variables
# ---------------------------
ifdef V
    VERBOSE = --verbose
    ifeq ($(V),2)
        TEST_VERBOSE = --verbose
        VERBOSE_SHORT = -vv
    else
        VERBOSE_SHORT = -v
    endif
else
    QUIET = --quiet
endif

install_args =
ifdef DESTDIR
	install_args += --root="$(DESTDIR)"
	export DESTDIR
endif
install_args += --prefix="$(prefix)"
install_args += --disable-pip-version-check

PYTEST_FLAGS = $(QUIET) $(TEST_VERBOSE)

PYTHON_DIRS = mockfs

# Site configuration goes in untracked config.mak
-include config.mak

.PHONY: install
install:: all
	$(PIP) $(QUIET) $(VERBOSE) install $(install_args) .

test: all
	$(PYTEST) $(PYTEST_FLAGS) $(flags) $(PYTHON_DIRS)

tox:
	$(TOX) --skip-missing-interpreters -e 'py{36,37,38,39,310,311}'

.PHONY: fmt
fmt::
	$(GIT) ls-files -- '*.py' | $(XARGS) $(CERCIS)

.PHONY: all install tags test
