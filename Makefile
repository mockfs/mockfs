# The default target of this Makefile is...
.PHONY: all
all::

# Development
# -----------
# make V=1                      # V=1 increases verbosity
# make test [flags=...]         # run tests; flags=-x fails fast, --ff failed first
# make test V=2                 # run tests; V=2 increases test verbosity

# Installation
# ------------
# "prefix" (and, optionally, "DESTDIR") can be passed on the command-line when installing, e.g.
#     make DESTDIR=/tmp/stage prefix=/usr install
prefix ?= $(CURDIR)/dist/mockfs
# DESTDIR =

# Commands
# --------
# The external commands used by this Makefile are...
PIP = pip
PYTHON ?= python
PYTEST ?= $(PYTHON) -m pytest

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

PYTEST_FLAGS = -p no:cacheprovider --doctest-modules
PYTEST_FLAGS += $(QUIET) $(TEST_VERBOSE)

PYTHON_DIRS = mockfs
PYTHON_DIRS += tests

# Site configuration goes in untracked config.mak
-include config.mak

.PHONY: install
install:: all
	$(PIP) $(QUIET) $(VERBOSE) install $(install_args) .

test: all
	$(PYTEST) $(PYTEST_FLAGS) $(flags) $(PYTHON_DIRS)
