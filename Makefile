# The default target of this Makefile is...
.PHONY: all
all::

# Installation
# ------------
# "prefix" (and, optionally, "DESTDIR") can be passed on the command-line when installing, e.g.
# make DESTDIR=/tmp/stage prefix=/usr install
prefix ?= $(CURDIR)/dist/mockfs
# DESTDIR =

# Commands
# --------
# The external commands used by this Makefile are...
PIP = pip

# Flags and Control Variables
# ---------------------------
ifdef V
    VERBOSE = --verbose
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

# Site configuration goes in untracked config.mak
-include config.mak

.PHONY: install
install:: all
	$(PIP) $(QUIET) $(VERBOSE) install $(install_args) .
