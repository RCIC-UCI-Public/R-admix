# Copyright (c) 2000 - 2019 The Regents of the University of California.
# All rights reserved.	
# This includes the Generic yaml2rpm Makefile - most packaging should
# be able to use this.
ALL_TARGETS = all
include $(YAML2RPM_HOME)/sys/Makefile

SHELL = /bin/bash
TMPYAMLS = $(shell find . -maxdepth 1 -name '*.yaml' -not -name R.yaml -not -name R-module.yaml -not -name builddeps.yaml -not -name r-pkg.yaml)

all: modules.bootstrap bootstrap R_versions.yaml prep 
	make BOOTSTRAP_MODULES_FILE=modules.bootstrap2 bootstrap

prep: modules.build 
	./downloadpkg.py

builddeps.yaml: modules.desired deps.R
	( module load R; \
	  cat deps.R | R --slave > $@  )

R_versions.yaml: outversions.yaml 
	cat outversions.yaml $@.base > $@

buildorder outversions.yaml: builddeps.yaml 
	./depend.py > buildorder

modules.bootstrap2: buildorder 
	cat modules.bootstrap.base buildorder  > modules.bootstrap2

modules.bootstrap:
	cat $@.base > $@

modules.build: modules.bootstrap2 
	cat modules.bootstrap2 > $@
	
clean:
	-/bin/rm modules.bootstrap modules.bootstrap2 modules.build
	-/bin/rm $(TMPYAMLS)
	-/bin/rm buildorder
	
veryclean:
	-/bin/rm builddeps.yaml
