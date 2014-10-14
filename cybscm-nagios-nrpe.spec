# main header info

Name:                   cybscm-nrpe-cfg 
Summary:                Cybs Nagios NRPE Config Files.
Version:                1.0
Release:                1
License:		CyberSource License (Proprietary)
Group:			Applications/Servers
BuildArch:		noarch
Buildroot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv:		no
Provides: 		cybscm-nrpe-cfg = %{version}-%{release}

# turn debugging off - we are not building anything.
%define debug_package	%{nil}

# description for the main package
%description
This package provides the new Cybs Specific Nagios/NRPE config files

%prep
# setup macro:
# -c = create a dummy toplevel
# -T = do not automatically unpack Source0 into source dir.
%setup -c -T

%install
# create directories where the files will be located
mkdir -p $RPM_BUILD_ROOT/etc/nagios/
mkdir -p $RPM_BUILD_ROOT/usr/lib64/nagios/plugins/

cp /home/narthur/cybs-nagios/nrpe.cfg_cybs $RPM_BUILD_ROOT/etc/nagios/
cp /home/narthur/cybs-nagios/check_hosts.sh $RPM_BUILD_ROOT/usr/lib64/nagios/plugins/
cp /home/narthur/cybs-nagios/check_dir_owner $RPM_BUILD_ROOT/usr/lib64/nagios/plugins/
cp /home/narthur/cybs-nagios/check_lsof $RPM_BUILD_ROOT/usr/lib64/nagios/plugins/

%pre
echo ""
echo "-----------------------------------------"
echo "Config Pre-Install Phase"
echo "-----------------------------------------"
echo "Adding new cybs specifc config file and additional nrpe scripts"

%post
echo ""
echo "-----------------------------------------"
echo "Config Post-Install Phase"
echo "-----------------------------------------"
mv /etc/nagios/nrpe.cfg /etc/nagios/nrpe.cfg_orig
mv /etc/nagios/nrpe.cfg_cybs /etc/nagios/nrpe.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%preun
if [ "$1" = "0" ]; then
  # This is an uninstall
echo "Uninstalling RPM"
fi
exit 0

%postun
if [ "$1" = "0" ]; then
  # This is an uninstal
#cp /etc/nagios/nrpe.cfg_orig /etc/nagios/nrpe.cfg
echo "Uninstalling RPM"
fi
exit 0

%files
%defattr(755,root,root)
/usr/lib64/nagios/plugins/check_hosts.sh
/usr/lib64/nagios/plugins/check_dir_owner
/usr/lib64/nagios/plugins/check_lsof
%attr(644, root, root) /etc/nagios/nrpe.cfg_cybs


%changelog
* Mon Oct 13 2014 Nigel Arthur <narthur@visa.com> 1.0.1
- initial package.

