# source stream
%define accurev_stream	DevTools_Integration_Lane

# main header info
Name:                   NrpeSetupR1Regressions
Summary:                Nrpe for Nagios Monitoring of R1 environments.
Version:                1
Release:                2
License:		CyberSource License (Proprietary)
Group:			Applications/Servers
BuildArch:		noarch
Buildroot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv:		no
Provides: 		cybscm-nrpe-R1-environments-config = %{version}-%{release}
Requires:		nagios-nrpe
Requires: 		nagios-plugins




# turn debugging off - we are not building anything.
%define debug_package	%{nil}

# description for the main package
%description
This package installs Nrpe to a regression environment and uses the hosts file to configures itself to speak to nagios server(installed on hotwas server)

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

mkdir -p $RPM_BUILD_ROOT/etc/nagios/tmp
mkdir -p $RPM_BUILD_ROOT/usr/lib64/nagios/plugins

# populate source dir from AccuRev rh5_templates
accurev pop -R -v %{accurev_stream} -L $RPM_SOURCE_DIR /./puppet/modules/nrpe/files

rsync -aplx --link-dest=$RPM_SOURCE_DIR/puppet/modules/nrpe/files $RPM_SOURCE_DIR/puppet/modules/nrpe/files $RPM_BUILD_ROOT/etc/nagios/tmp

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

echo 'creating nrpe user'
/usr/sbin/adduser nrpe
echo "Renaming pre-delivered files before installing cybs specific versions"

mv /etc/nagios/nrpe.cfg /etc/nagios/nrpe.cfg_old

#SEE IF THERE IS A BETTER WAY TO DO THIS FOR CHECK_* PLUGINS
cp /etc/nagios/tmp/files/nrpe.cfg /etc/nagios/
cp /etc/nagios/tmp/files/check_* /usr/lib64/nagios/plugins
chown -R nagios:nagios /etc/nagios/
chown -R nagios:nagios /usr/lib64/nagios/plugins
echo "Extracting variables from /etc/hosts"
HOTNTA=$(ping -c 1 hotnta | grep PING | awk '{print $3}' | sed 's/(//' | sed 's/)//')

echo "Populating values from /etc/hosts to Nagios host file definations to enable monitoring"
sed -i "/allowed_hosts/s|$|,$HOTNTA|" /etc/nagios/nrpe.cfg

echo 'Adding Nagios User to Sudoers list with limited rights to enable running of check_dns'
echo 'nagios ALL=(ALL) NOPASSWD:/usr/lib64/nagios/plugins/check_hosts.sh' >> /etc/sudoers
echo "Starting NRPE Service and adding to init.d"
/sbin/service nrpe restart > /dev/null 2>&1
/sbin/chkconfig nrpe on

%preun
if [ "$1" = "0" ]; then
  # This is an uninstall

echo "reverting back Nrpe installation files from cybs specific versions"
mv /etc/nagios/nrpe.cfg_old /etc/nagios/nrpe.cfg
fi
exit 0

%postun
if [ "$1" = "0" ]; then
  # This is an uninstal
echo "Removing Nagios directories"
rm -rf /etc/nagios
rm -rf /usr/lib64/nagios
echo "Removing Nagios and NRPE services from runlevels"
/sbin/chkconfig --del nrpe > /dev/null 2>&1

fi
exit 0

%files
%defattr(-,root,root)
%attr(-,nagios,nagios) /etc/nagios/
%attr(-,nagios,nagios) /usr/lib64/nagios/plugins


%changelog

* Thu Jul 18 2013 Nigel Arthur <narthur@visa.com> 1.2
- Changed file locations

* Fri Jul 12 2013 Nigel Arthur <narthur@visa.com> 1.1
- initial package.

