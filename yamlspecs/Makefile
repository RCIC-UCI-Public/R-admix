# Copyright (c) 2000 - 2019 The Regents of the University of California.
# All rights reserved.	
# This includes the Generic yaml2rpm Makefile - most packaging should
# be able to use this.
ALL_TARGETS = all
include $(YAML2RPM_HOME)/sys/Makefile

SHELL = /bin/bash

.PHONY: force

## when cleaning temporary yaml files, figure out which ones to not remove
KEEPYAMLS0 = $(shell cat modules.bootstrap.base)
KEEPYAMLS0 = $(shell cat keepyamls)
KEEPYAMLS0 += r-pkg R_versions
KEEPYAMLS = $(patsubst %,%.yaml,$(KEEPYAMLS0))
TMPYAMLS0 = $(wildcard *.yaml)
TMPYAMLS = $(filter-out $(KEEPYAMLS),$(TMPYAMLS0))

all: modules.bootstrap versions.yaml bootstrap R_versions.yaml prep 
	make BOOTSTRAP_MODULES_FILE=modules.bootstrap2 bootstrap
	make modules.manifest
        
prep: modules.build 
	./downloadpkg.py

builddeps.yaml: modules.desired deps.R
	( module load R; \
	  cat deps.R | R --slave > $@  )
	cat $@.base >> $@

R_versions.yaml: outversions.yaml 
	rm -rf versions.yaml
	cat outversions.yaml $@.base > $@
	cat outversions.yaml $@.base > versions.yaml
	

versions.yaml: 
	cat R_versions.yaml.base > $@

buildorder outversions.yaml: builddeps.yaml 
	./depend.py > buildorder

modules.bootstrap2: buildorder 
	cat modules.bootstrap.base buildorder  > modules.bootstrap2

modules.bootstrap:
	cat $@.base > $@

modules.build: modules.bootstrap2 
	cat modules.bootstrap2 > $@

manifest: modules.manifest

modules.manifest: force
	cat modules.bootstrap2 >$@
	
freeze:
	echo "freezing all yaml files, bootstrap files, buildorder into freeze subdir"
	if [ ! -d freeze ]; then mkdir freeze; fi
	cp -p *yaml *bootstrap* modules.build buildorder freeze
clean:
	-/bin/rm modules.bootstrap modules.bootstrap2 modules.build
	-/bin/rm $(TMPYAMLS)
	-/bin/rm buildorder
	-/bin/rm builddeps.yaml 
	
veryclean:
	-/bin/rm builddeps.yaml

