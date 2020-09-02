# Copyright (c) 2000 - 2019 The Regents of the University of California.
# All rights reserved.	
# This includes the Generic yaml2rpm Makefile - most packaging should
# be able to use this.
SUBMAKES = Makefile.R3 Makefile.R4
.DEFAULT_GOAL = default
%.pkg: %.yaml
	for f in $(SUBMAKES); do \
		if [ -f $@ ] ; then /bin/rm $@; fi; \
		$(MAKE) -f $$f R_versions.yaml $@; \
        done
	
manifest module-provides module-requires: 
	for f in $(SUBMAKES); do \
		$(MAKE) -s -f $$f R_versions.yaml modules.bootstrap2 $@; \
        done

ansible freeze: force
	for f in $(SUBMAKES); do \
		$(MAKE) -s -f $$f R_versions.yaml $@; \
        done

download:
	echo "Use a specific Makefile from $(SUBMAKES) to download packages"

%: 	
	$(MAKE) -f Makefile.R3 $*
	$(MAKE) -f Makefile.R3 clean
	$(MAKE) -f Makefile.R4 $*
