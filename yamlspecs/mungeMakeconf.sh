#!/bin/bash
# This is horrendous. For a single package, rstan, we need the following definitions in the *system* Makeconf
# file. We need it only for this package and hence we do some "munging" of the system version
# and then restore the old one. This is dangerous. It's possible to completely screw up the system
# RPM. Never do this. 
# call as:
#    mungeMakeconf.sh [save|restore|verify]
RSTANCOMPILERDEFS="
CXX14 = g++ \n
CXX14FLAGS = -Wno-unused-variable \$(LTO) \n
CXX14PICFLAGS = -fPIC \n
CXX14STD = -std=c++1y 
"
MAKECONF=$(pkg-config --variable=rhome libR)/etc/Makeconf
RPACKAGE=`rpm -qf $(pkg-config --variable=rhome libR)`
TMPMAKECONF=./Makeconf


save () {
  [ -f $TMPMAKECONF ] && /bin/rm $TMPMAKECONF
  echo "Saving $MAKECONF to $TMPMAKECONF"
  /bin/cp -p $MAKECONF $TMPMAKECONF
}

restore () {
  if [ -f $TMPMAKECONF ]; then 
     echo "restoring $TMPMAKECONF to $MAKECONF"
     /bin/cp -p $TMPMAKECONF $MAKECONF
  fi
}

verify() {
  rpm --verify $RPACKAGE
}

if [ "$1" == "munge" ]; then
  save
  echo -e $RSTANCOMPILERDEFS >> $MAKECONF
fi

[ "$1" == "restore" ] &&  restore
[ "$1" == "verify" ] &&  verify

