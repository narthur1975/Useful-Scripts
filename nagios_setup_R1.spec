# source stream
%define accurev_stream	DevTools_Integration_Lane

# main header info
Name:                   NagiosSetupR1Regressions
Summary:                Nagios Monitoring for R1 environments.
Version:                2
Release:                3
License:		CyberSource License (Proprietary)
Group:			Applications/Servers
BuildArch:		noarch
Buildroot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv:		no
Provides: 		cybscm-nagios-R1-environments-config = %{version}-%{release}
Requires:		nagios
Requires:		nagios-nrpe
Requires: 		nagios-plugins-nrpe




# turn debugging off - we are not building anything.
%define debug_package	%{nil}

# description for the main package
%description
This package installs Nagios to a regression environment and using the hosts file configures itself to monitor all associated regression environments

%prep
# setup macro:
# -c = create a dummy toplevel
# -T = do not automatically unpack Source0 into source dir.
%setup -c -T

%install
# clear down buildroot
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

# clear down sourcedir
rm -rf $RPM_SOURCE_DIR
mkdir -p $RPM_SOURCE_DIR

mkdir -p $RPM_BUILD_ROOT/etc/nagios/cybsni
mkdir -p $RPM_BUILD_ROOT/etc/nagios/tmp
mkdir -p $RPM_BUILD_ROOT/usr/lib64/nagios/plugins

# populate source dir from AccuRev rh5_templates
accurev pop -R -v %{accurev_stream} -L $RPM_SOURCE_DIR /./nagios/nagios-regressions

rsync -aplx --link-dest=$RPM_SOURCE_DIR/nagios/nagios-regressions/ $RPM_SOURCE_DIR/nagios/nagios-regressions/ $RPM_BUILD_ROOT/etc/nagios/tmp

%clean
# remove buildroot
rm -rf $RPM_BUILD_ROOT

%pre
echo ""
echo "-----------------------------------------"
echo "Config Pre-Install Phase"

echo "-----------------------------------------"

%post
echo ""
echo "-----------------------------------------"
echo "Config Post-Install Phase"
echo "-----------------------------------------"

echo 'adding nrpe to /etc/services(if it is not already there'
grep -qi nrpe /etc/services || echo "nrpe            5666/tcp              # NRPE"  >> /etc/services

echo "Renaming pre-delivered files before installing cybs specific versions"

mv /etc/nagios/objects/commands.cfg /etc/nagios/objects/commands.cfg_old
mv /etc/nagios/objects/localhost.cfg /etc/nagios/objects/localhost.cfg_old
cp /etc/nagios/tmp/objects/commands.cfg /etc/nagios/objects/
cp /etc/nagios/tmp/objects/localhost.cfg /etc/nagios/objects/
cp /etc/nagios/tmp/cybsni/* /etc/nagios/cybsni
cp /etc/nagios/tmp/htpasswd.users /etc/nagios
mv /etc/nagios/nagios.cfg  /etc/nagios/nagios.cfg_old 
cp /etc/nagios/tmp/nagios.cfg /etc/nagios/
echo "Extracting variables from /etc/hosts"
HOTSIM=$(ping -c 1 hotsim | grep PING | awk '{print $3}' | sed 's/(//' | sed 's/)//')
CTE=$(ping -c 1 cte | grep PING | awk '{print $3}' | sed 's/(//' | sed 's/)//')
#HOTNTA=$(ping -c 1 hotnta | grep PING | awk '{print $3}' | sed 's/(//' | sed 's/)//')
HOTMQ=$(ping -c 1 hotmq | grep PING | awk '{print $3}' | sed 's/(//' | sed 's/)//')
HOTWAS=$(ping -c 1 hotwas | grep PING | awk '{print $3}' | sed 's/(//' | sed 's/)//')
echo "Populating values from /etc/hosts to Nagios host file definations to enable monitoring"
sed -i "s/FE_HOSTNAME/$HOSTNAME/" /etc/nagios/cybsni/services-mq.cfg 
sed -i "s/CTE_IP/$CTE/" /etc/nagios/cybsni/host-cte.cfg 
sed -i "s/LISTENERS_IP/$HOTSIM/" /etc/nagios/cybsni/host-listeners.cfg 
sed -i "s/MQ_IP/$HOTMQ/" /etc/nagios/cybsni/host-mq.cfg
sed -i "s/WAS_IP/$HOTWAS/" /etc/nagios/cybsni/host-was.cfg

echo "Starting Nagios Service and adding to init.d"
/sbin/service nagios restart > /dev/null 2>&1
/sbin/chkconfig nagios on
echo "Starting NRPE Service and adding to init.d"
/sbin/service nrpe restart > /dev/null 2>&1
/sbin/chkconfig nrpe on

%preun
if [ "$1" = "0" ]; then
  # This is an uninstall
echo "reverting back Nagios installation files from cybs specific versions"
mv /etc/nagios/objects/commands.cfg_old /etc/nagios/commands.cfg
mv /etc/nagios/objects/localhost.cfg_old /etc/nagios/localhost.cfg
rm /etc/nagios/nagios.cfg
mv /etc/nagios/nagios.cfg_old /etc/nagios/nagios.cfg
fi
exit 0

%postun
if [ "$1" = "0" ]; then
  # This is an uninstal
echo "Removing Nagios directories"
rm -rf /etc/nagios
rm -rf /usr/lib64/nagios
echo "Removing Nagios and NRPE services from runlevels"
/sbin/chkconfig --del nagios > /dev/null 2>&1
/sbin/chkconfig --del nrpe > /dev/null 2>&1

fi
exit 0

%files
%defattr(-,root,root)
%attr(-, nagios, nagios) /etc/nagios/
%attr(-, nagios, nagios) /usr/lib64/nagios/plugins

%changelog
* Tue Jul 16 2013 Nigel Arthur <narthur@visa.com> 2.3
- Changed directory ownership for files delivered to Nagios from root

* Tue Jul 16 2013 Nigel Arthur <narthur@visa.com> 2.2
- Changed Nagios server from HOTWAS vm to FE vm so can use $HOSTNAME value for MQ monitoring

* Mon Jul 12 2013 Nigel Arthur <narthur@visa.com> 2.1
- Added in rpm pre-requisites for initial Nagios installation prior to cybs specific setup

* Mon Jul 11 2013 Nigel Arthur <narthur@visa.com> 1.1
- initial package.

