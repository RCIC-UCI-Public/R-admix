## Read the files "modules.desired" to generate a YAML file 
## of all packages and dependencies. This uses the miniCRAN 
## module, which does recursive dependency resolution.
## This file can then be processed to determine the build/bootstrap order
## of R RPMs, it can also be used to place dependencies in R module RPMs

library(miniCRAN)
allPkgs <- available.packages(repos="https://cran.r-project.org")
pkgList <- readLines("modules.desired") 
allDeps <- pkgDep(pkgList, availPkgs=allPkgs, suggests=FALSE) 
allDeps <- unique(allDeps)

cat(sprintf("## %d desired --> %d required\n", length(pkgList), length(allDeps)))
cat(sprintf("---\n"))
for (pkg in allDeps) 
{
	deps <- pkgDep(pkg,availPkgs=allPkgs,suggests=FALSE)
        pkgInfo = allPkgs[allPkgs[,"Package"] %in% pkg,]
	cat(sprintf("%s : \n",deps[1]))
	cat(sprintf("  version : \"%s\"\n",pkgInfo["Version"]))
	cat(sprintf("  requires : \n"))
        if ( length(deps) == 1 )
	 	next	
        for (i in 2:length(deps))
            cat(sprintf("    - %s\n",deps[i]))
}
