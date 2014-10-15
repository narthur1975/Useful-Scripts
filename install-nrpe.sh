#!/bin/bash
set -x
fail () {
  echo "OH NOES! It failed while $1"
  exit 1
}


kernel=$(uname -r)
version1=el5
version2=el6

echo "$kernel" | grep -q "$version1"
if [[ $? == 0 ]] ;
then echo Version is el5
yum install -y nagios-plugins-1.4.15-2.el5.rf 
[[ $? == "0" ]] || fail "installing nagios-plugins package"
yum install -y  nagios-nrpe-2.12-1.el5.rf
[[ $? == "0" ]] || fail "installing nagios-nrpe package"
yum install -y cybscm-nrpe-cfg.el5-1.0-1
[[ $? == "0" ]] || fail "Installing Cybs NRPE Package"
sed -i '$a nrpe  5666/tcp  # NRPE' /etc/services
[[ $? == "0" ]] || fail "Updating /etc/services file"
/sbin/chkconfig nrpe on
[[ $? == "0" ]] || fail "Adding service to chkconfig"
/sbin/service nrpe start
[[ $? == "0" ]] || fail "Starting NRPE Service"
echo "NRPE Service with CYBS Specific config files sucessfully installed and started"
fi

echo "$kernel" | grep -q "$version2"
if [[ $? == 0 ]] ; 
then echo version is el6
yum install -y  nagios-nrpe-2.14-1.el6.rf
[[ $? == "0" ]] || fail "installing nagios-nrpe package"
yum install -y cybscm-nrpe-cfg.el6-1.0-1
[[ $? == "0" ]] || fail "Installing Cybs NRPE Package"
sed -i '$a nrpe  5666/tcp  # NRPE' /etc/services
[[ $? == "0" ]] || fail "Updating /etc/services file"
/sbin/chkconfig nrpe on
[[ $? == "0" ]] || fail "Adding service to chkconfig"
/sbin/service nrpe start
[[ $? == "0" ]] || fail "Starting NRPE Service"
echo "NRPE Service with CYBS Specific config files sucessfully installed and started"
fi
