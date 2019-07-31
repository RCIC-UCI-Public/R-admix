#!/usr/bin/env python
import re
import sys
import subprocess
R_MODULE = "R/3.6.1"
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

RTEMPLATE = """
module load %s;
echo 'download.packages("%s",destdir="../sources", repos="https://cran.r-project.org")' | R --slave
"""

RDEPENDS = """
module load %s;
echo 'download.depedencies("%s",check=FALSE, deplevel="Depends")' | R --slave
"""

## This are recommend packages from R-Studio's list of useful packages
## https://support.rstudio.com/hc/en-us/articles/201057987-Quick-list-of-useful-R-packages 
groups= {}
groups['system'] = ["xts", "TTR", "curl"]
groups['system'].extend([ 'digest', 'gtable', 'lazyeval', 'reshape2', 'rlang', 'scales', 'tibble', 'viridisLite', 'withr'])
groups['system'].extend([ 'plyr', 'Rcpp', 'stringr']) 
groups['system'].extend(['glue', 'magrittr', 'stringi'])
groups['system'].extend(['assertthat','crayon', 'cli', 'fansi', 'pillar'])
groups['system'].extend(['utf8', 'vctrs'])
groups['system'].extend(['pkgconfig','backports', 'ellipsis', 'zeallot'])
groups['system'].extend(['labeling', 'munsell', 'R6', 'RColorBrewer'])
groups['system'].extend(['colorspace'])
groups['system'].extend(['purrr','tidyselect', 'BH', 'plogr','dplyr'])
groups['system'].extend(['httpuv', 'mime', 'jsonlite', 'xtable', 'htmltools', 'sourcetools', 'later', 'promises'])
groups['system'].extend(['yaml','htmlwidgets', 'knitr', 'crosstalk', 'manipulateWidget'])
groups['system'].extend(['evaluate', 'highr', 'markdown', 'xfun'])
groups['system'].extend(['miniUI', 'base64enc', 'webshot'])
groups['system'].extend(['ps','processx','callr'])
groups['system'].extend(['gridExtra','png', 'raster', 'sp', 'viridis'])
groups['system'].extend(['prettyunits','igraph','blob', 'bit','bit64', 'hms'])
groups['system'].extend(['memoise'])
groups['system']= ['sys','askpass','openssl', 'httr', 'XML', 'miniCRAN']
groups['dataload']=["odbc","RMySQL", "RSQLite","RPostgreSQL"]
groups['dataload'].extend(["XLConnect","xlsx","foreign","haven"])
groups['datamanip']=["dplyr","tidyr","stringr","lubridate"]
groups['dataviz']=["ggplot2","ggvis","rgl","htmlwidgets"]
groups['dataviz'].extend(["shape","igraph","magrittr","leaflet","dygraphs","DT","diagram","networkD3","threejs","googleVis"])
groups['datamodel']=["car","mgcv","lme4","nlme","randomForest","multcomp","vcd"]
groups['datamodel'].extend(["glmnet","survival","caret"])
groups['datareport']=["shiny","xtable"]
groups['dataspatial']=["sp","maptools","maps","ggmap"]
groups['datatime']=["zoo","xts","quantmod"]
groups['codeperf']=["Rcpp","data.table","Rmpi"]


pkgs = []
for g in groups.keys():
	pkgs.extend(groups[g])

pkgs = groups['system']
for pkg in pkgs:
        print pkg
        proc = subprocess.Popen(["/bin/bash"],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (output,err) = proc.communicate(RTEMPLATE % (R_MODULE,pkg))
        m=re.search("https:.*%s_.*.tar.gz" % pkg,output)
        version=m.group(0).split("%s_"% pkg)[1].split(".tar.gz")[0]
        r=re.search("-",version)
        if r is None:
           template = YAMLTEMPLATE
        else:
           (version,release) = version.split('-')
           print '%s_release: "%s"' % (pkg,release)
           template = YAMLTEMPLATE_RELEASE
        print '%s: "%s"' % (pkg,version)

        with open("%s.yaml" % pkg,"w") as f:
        	contents=re.sub("MODULE", pkg, template) 
        	f.write(contents)

