#!/usr/bin/env python
import re
import sys
import subprocess
import yaml
from os import path
BUILDDEPS = "builddeps.yaml"
R_MODULE = "R/3.6.2"
RTEMPLATE = """
module load %s;
echo 'download.packages("%s",destdir="../sources", repos="https://cran.r-project.org")' | R --slave
"""

f = open(BUILDDEPS,"r")
allPkgs = yaml.load(f)

for pkg in allPkgs.keys():
	
	if not path.exists("../sources/%s_%s.tar.gz" % (pkg, allPkgs[pkg]['version'])): 
		print "downloading package %s" % pkg
        	proc = subprocess.Popen(["/bin/bash"],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        	(output,err) = proc.communicate(RTEMPLATE % (R_MODULE,pkg))

