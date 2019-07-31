#!/usr/bin/env python
import re
import sys
import subprocess
R_VERSION = "3.6.1"
R_MODULE = "R/%s" % R_VERSION
YAMLTEMPLATE="""
!include r-pkg.yaml
---
- package: R module MODULE
  name: MODULE
  version: "{{ versions.MODULE }}"
  src_tarball: "{{name}}_{{version}}.{{extension}}"
  vendor_source: https://cran.r-project.org/src/contrib/{{name}}_{{version}}.tar.gz 
"""
YAMLTEMPLATE_RELEASE="""

!include r-pkg.yaml
---
- package: R module MODULE
  name: MODULE
  version: "{{ versions.MODULE }}"
  release: "{{versions.MODULE_release }}"
  src_tarball: "{{name}}_{{version}}-{{release}}.{{extension}}"
  vendor_source: https://cran.r-project.org/src/contrib/{{name}}_{{version}}-{{release}}.tar.gz 
"""

class Node(object):
	def __init__(self,name):
		self.name = name
		self.pkgname = self.name.replace(".","_")
		self.edges = []
	def addEdge(self, node):
		self.edges.append(node)

	def resolve(self,resolved):
		for edge in self.edges:
                          if edge not in resolved:
			  	edge.resolve(resolved)
		resolved.append(self)

import yaml
f=open("builddeps.yaml")
r_modules = yaml.load(f)

syspkgs = ["lattice", "Matrix"]

# Create Graph nodes for every module
nodes = [ Node(name) for name in r_modules]

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
           print pkg.pkgname
           r=re.search("-",version)
           if r is None:
              template = YAMLTEMPLATE
           else:
              (version,release) = version.split('-')
              yamlversions.write('%s_release: "%s"\n' % (pkg.pkgname,release))
              template = YAMLTEMPLATE_RELEASE
           yamlversions.write('%s: "%s"\n' % (pkg.pkgname,version))
   
           with open("%s.yaml" % pkg.pkgname,"w") as f:
              contents=re.sub("MODULE", pkg.pkgname, template) 
              f.write(contents)
              deps = r_modules[pkg.name]['requires']
              f.write("  requires:\n") 
              f.write("    - R_%s\n" % R_VERSION)
              try:
                  for p in deps:
                      if p not in syspkgs:
                          f.write("    - %s_R_%s\n" % (p.replace(".","_"),R_VERSION))
              except:
                  pass
	except: 
               pass

yamlversions.close()
