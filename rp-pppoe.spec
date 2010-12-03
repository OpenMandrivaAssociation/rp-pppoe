%define enable_debug	0
%{?_with_debug: %global enable_debug 1}
%{?_without_debug: %global use_debug 0}

%define pppver	2.4.5

Summary:	ADSL/PPPoE userspace driver
Name:		rp-pppoe
Version:	3.10
Release:	%mkrel 3
Source0:	http://www.roaringpenguin.com/files/download/%{name}-%{version}.tar.gz
Source3:	http://www.luigisgro.com/sw/rp-pppoe-3.8.patch/README-first-session-packet-lost.txt
Patch0:		rp-pppoe-3.8-CAN-2004-0564.patch
Url:		http://www.roaringpenguin.com/pppoe
License:	GPL
Group:		System/Servers
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	ppp >= 2.4.1
BuildRequires:	autoconf2.5
BuildRequires:	ppp-devel = %{pppver}

%package	gui
Group:		System/Servers
Summary:	GUI front-end for rp-pppoe
Requires:	rp-pppoe >= 3.6
Requires:	tk

%description
PPPoE (Point-to-Point Protocol over Ethernet) is a protocol used by
many ADSL Internet Service Providers. Roaring Penguin has a free
client for Linux systems to connect to PPPoE service providers.

The client is a user-mode program and does not require any kernel
modifications. It is fully compliant with RFC 2516, the official PPPoE
specification.

It has been tested with many ISPs, such as the Canadian Sympatico HSE (High
Speed Edition) service.

%description	gui
This package contains the graphical frontend (tk-based) for rp-pppoe.

Install this if you wish to have a graphical frontend for pppoe.

%package	plugin
Summary:	PPP over ethernet kernel-mode plugin
Group:		System/Servers
Requires:	%{name} = %{version}
Conflicts:	ppp-pppoe

%description	plugin
PPP over ethernet kernel-mode plugin.

%prep
%setup -q
%patch0 -p1 -b .CAN

%build
%serverbuild
cd src
autoconf
%if %enable_debug
CFLAGS="$RPM_OPT_FLAGS -g" \
%endif
%configure2_5x --docdir=%{_docdir}/%{name} \
	--enable-plugin=%{_includedir} --docdir=%{_docdir}/%{name}

%make

perl -pi -e 's|/etc/ppp/plugins/|%{_libdir}/pppd/%{pppver}|g' \
	doc/KERNEL-MODE-PPPOE

%install
rm -fr %buildroot
install -d -m 0755 %buildroot
install -m 644 %{SOURCE3} ./README-first-session-packet-lost.txt

pushd src
%makeinstall_std
popd

pushd gui
%makeinstall_std
popd

# This is necessary for the gui to work, but it shouldn't be done here !
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ppp/rp-pppoe-gui

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-rp-pppoe-gui.desktop <<EOF
[Desktop Entry]
Name=TkPPPoE
Comment=Frontend for rp-pppoe
Exec=%{_bindir}/tkpppoe
Icon=remote_access_section
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Internet-RemoteAccess;Network;RemoteAccess;Dialup;
EOF

perl -pi -e "s/restart/restart\|reload/g;" %{buildroot}%{_initrddir}/pppoe
rm -rf %{buildroot}/usr/share/doc

mkdir -p $RPM_BUILD_ROOT%{_libdir}/pppd/%{pppver}
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/ppp/plugins/README
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/ppp/plugins/rp-pppoe.so \
	$RPM_BUILD_ROOT%{_libdir}/pppd/%{pppver}/

# backward compatibility links
for i in connect start stop setup status; do
	ln -sf %{_sbindir}/pppoe-$i $RPM_BUILD_ROOT%{_sbindir}/adsl-$i
	ln -sf pppoe-$i.8 $RPM_BUILD_ROOT%{_mandir}/man8/adsl-$i.8
done

%if %enable_debug
export DONT_STRIP=1
export EXCLUDE_FROM_STRIP=".*"
%endif

%clean
rm -fr %buildroot

%post gui
%if %mdkversion < 200900
%update_desktop_database
%update_menus
%endif

%postun gui
%if %mdkversion < 200900
%clean_desktop_database
%clean_menus
%endif


%files
%defattr(-,root,root)
%doc doc/* README SERVPOET
%doc README-first-session-packet-lost.txt
%config(noreplace) %{_sysconfdir}/ppp/pppoe.conf
%config(noreplace) %{_sysconfdir}/ppp/pppoe-server-options
%config(noreplace) %{_sysconfdir}/ppp/firewall-masq
%config(noreplace) %{_sysconfdir}/ppp/firewall-standalone
%{_sbindir}/pppoe
%{_sbindir}/pppoe-connect
%{_sbindir}/pppoe-relay
%{_sbindir}/pppoe-server
%{_sbindir}/pppoe-setup
%{_sbindir}/pppoe-sniff
%{_sbindir}/pppoe-start
%{_sbindir}/pppoe-status
%{_sbindir}/pppoe-stop
%{_sbindir}/adsl-connect
%{_sbindir}/adsl-setup
%{_sbindir}/adsl-start
%{_sbindir}/adsl-status
%{_sbindir}/adsl-stop
%{_mandir}/man[58]/*
%config(noreplace)%{_initrddir}/pppoe

%files gui
%defattr(-,root,root)
%{_bindir}/tkpppoe
%{_sbindir}/pppoe-wrapper
%{_mandir}/man1/*
%if %{mdkversion} >= 200610
%{_datadir}/applications/*
%endif
%dir %{_datadir}/tkpppoe
%dir %{_sysconfdir}/ppp/rp-pppoe-gui
%{_datadir}/tkpppoe/*

%files plugin
%defattr(-,root,root)
%doc doc/KERNEL-MODE-PPPOE
%attr(755,root,root) %{_libdir}/pppd/%{pppver}/rp-pppoe.so


