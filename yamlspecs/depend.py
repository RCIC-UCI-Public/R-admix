#!/usr/bin/env python
from __future__ import print_function
import re
import sys
import subprocess
import yaml

R_VERSION = "3.6.1"
R_MODULE = "R/%s" % R_VERSION

YAMLTEMPLATE="""
!include r-pkg.yaml
---
- package: R module MODULE
  name: MODULE
  rpkgname: %s
  version: "{{ versions.MODULE }}"
  src_tarball: "{{rpkgname}}_{{version}}.{{extension}}"
  vendor_source: https://cran.r-project.org/src/contrib/{{rpkgname}}_{{version}}.tar.gz 
"""
YAMLTEMPLATE_RELEASE="""
!include r-pkg.yaml
---
- package: R module MODULE
  name: MODULE
  rpkgname: %s
  version: "{{ versions.MODULE }}"
  release: "{{versions.MODULE_release }}"
  src_tarball: "{{rpkgname}}_{{version}}-{{release}}.{{extension}}"
  vendor_source: https://cran.r-project.org/src/contrib/{{rpkgname}}_{{version}}-{{release}}.tar.gz 
"""
BUILD_OVERRIDE="""
  build:
    configure: echo no configure required
    pkgmake: echo installed with R CMD INSTALL
    target:
    modules:
      - R/{{versions.R}}
"""

addModules = { 'Rmpi': ['mpi/openmpi-x86_64'] }

def name_mangle(name):
    return name.replace(".","_")

class Node(object):
    def __init__(self,name):
        self.name = name
        self.pkgname = name_mangle(self.name)
        self.edges = []
    def addEdge(self, node):
        self.edges.append(node)

    def resolve(self,resolved):
        for edge in self.edges:
            if edge not in resolved:
                edge.resolve(resolved)
        resolved.append(self)



syspkgs = [ "KernSmooth", "MASS", "Matrix", "base", "boot", "class", "cluster", "codetools", \
"compiler", "datasets", "foreign", "grDevices", "graphics", "grid", "lattice", "methods", \
"mgcv", "nlme", "nnet", "parallel", "rpart", "spatial", "splines", "stats", "stats4", "survival", \
"tcltk", "tools", "translations", "utils" ] 

# Create Graph nodes for every module
f=open("builddeps.yaml")
r_modules = yaml.load(f)
nodes = [ Node(name) for name in r_modules.keys()]

# make a  master Node to and add all edges to it to make sure that the dependency graph is connected
master = Node('root node')
for node in nodes:
    if node.name not in syspkgs:
        master.addEdge(node)
    deps = r_modules[node.name]['requires']
    try:
        edges = filter(lambda x: x.name in deps, nodes)
        for edge in edges:
            if edge.name not in syspkgs:
                node.addEdge(edge)
    except:
        pass

resolved = []
# Resolve 
master.resolve(resolved)
yamlversions=open("outversions.yaml","w")
for pkg in resolved:
    try:
        version=r_modules[pkg.name]['version']
        print("%s" % pkg.pkgname)
        r=re.search("-",version)
        if r is None:
           template = YAMLTEMPLATE
        else:
           (version,release) = version.split('-')
           yamlversions.write('%s_release: "%s"\n' % (pkg.pkgname,release))
           template = YAMLTEMPLATE_RELEASE

        yamlversions.write('%s: "%s"\n' % (pkg.pkgname,version))

   
        with open("%s.yaml" % pkg.pkgname,"w") as f:
            contents=re.sub("MODULE", pkg.pkgname, template) % pkg.name 
            f.write(contents)
            deps = r_modules[pkg.name]['requires']
            f.write("  requires:\n") 
            f.write("    - R_%s\n" % R_VERSION)
            if deps is not None:
                for p in deps:
                    if p not in syspkgs:
                        f.write("    - R_%s-%s\n" % (R_VERSION,name_mangle(p)))

            if pkg.pkgname in addModules.keys():
		f.write(BUILD_OVERRIDE)
		for mod in addModules[pkg.pkgname]:
                    f.write("      - %s\n" % mod)
    except: 
        pass 

yamlversions.close()
