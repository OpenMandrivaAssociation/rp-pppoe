%define	pppver	2.4.5

%bcond_without	uclibc

Summary:	ADSL/PPPoE userspace driver
Name:		rp-pppoe
Version:	3.10
Release:	6
Source0:	http://www.roaringpenguin.com/files/download/%{name}-%{version}.tar.gz
Source3:	http://www.luigisgro.com/sw/rp-pppoe-3.8.patch/README-first-session-packet-lost.txt
Patch0:		rp-pppoe-3.8-CAN-2004-0564.patch
Patch1:		rp-pppoe-3.10-override-incompatible-compiler-and-linker-flags.patch
Patch2:		rp-pppoe-3.10-lsb.patch
Url:		http://www.roaringpenguin.com/pppoe
License:	GPLv2+
Group:		System/Servers
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

%if %{with uclibc}
%package -n	uclibc-pppoe
Summary:	uClibc-linked build of pppoe
Group:		System/Servers
BuildRequires:	uClibc-devel >= 0.9.33.2-3

%description -n	uclibc-pppoe
This package ships a build of pppoe linked against uClibc.

It's primarily targetted for inclusion with the DrakX installer.
%endif

%description	gui
This package contains the graphical frontend (tk-based) for rp-pppoe.

Install this if you wish to have a graphical frontend for pppoe.

%package	plugin
Summary:	PPP over ethernet kernel-mode plugin
Group:		System/Servers
Requires:	%{name} = %{EVRD}
Conflicts:	ppp-pppoe

%description	plugin
PPP over ethernet kernel-mode plugin.

%prep
%setup -q
%patch0 -p1 -b .CAN~
%patch1 -p1 -b .ldflags~
%patch2 -p1 -b .lsb~
cp %{SOURCE3} ./README-first-session-packet-lost.txt

%build
%serverbuild
cd src
%configure2_5x	--docdir=%{_docdir}/%{name} \
		--enable-plugin=%{_includedir} \
		--docdir=%{_docdir}/%{name}
%make

perl -pi -e 's|/etc/ppp/plugins/|%{_libdir}/pppd/%{pppver}|g' \
	doc/KERNEL-MODE-PPPOE

%if %{with uclibc}
%{uclibc_cc} -I. -o pppoe-uclibc pppoe.c if.c debug.c common.c ppp.c discovery.c -lcrypt -lutil -Wall -Wno-deprecated-declarations -DPPPOE_PATH='"/sbin/pppoe"' -DPPPD_PATH='"/sbin/pppd"' -DVERSION='"3.0-stg1"' %{uclibc_cflags} -Os -fwhole-program -flto %{ldflags} -Wl,-O2
%endif

%install
%makeinstall_std -C src

%makeinstall_std -C gui

%if %{with uclibc}
install -m755 src/pppoe-uclibc -D %{buildroot}%{uclibc_root}/sbin/pppoe
%endif

# This is necessary for the gui to work, but it shouldn't be done here !
mkdir -p %{buildroot}%{_sysconfdir}/ppp/rp-pppoe-gui

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-rp-pppoe-gui.desktop <<EOF
[Desktop Entry]
Name=TkPPPoE
Comment=Frontend for rp-pppoe
Exec=%{_bindir}/tkpppoe
Icon=remote_access_section
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Internet-RemoteAccess;Network;RemoteAccess;Dialup;
EOF

mkdir -p %{buildroot}%{_libdir}/pppd/%{pppver}
rm -f %{buildroot}%{_sysconfdir}/ppp/plugins/README
mv -f %{buildroot}%{_sysconfdir}/ppp/plugins/rp-pppoe.so \
	%{buildroot}%{_libdir}/pppd/%{pppver}/

%files
%doc README-first-session-packet-lost.txt
%doc %{_docdir}/%{name}-%{version}/*
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
%{_mandir}/man[58]/*.[58]*
%{_initrddir}/pppoe

%if %{with uclibc}
%files -n uclibc-pppoe
%{uclibc_root}/sbin/pppoe
%endif

%files gui
%{_bindir}/tkpppoe
%{_sbindir}/pppoe-wrapper
%{_mandir}/man1/*
%{_datadir}/applications/*
%dir %{_datadir}/tkpppoe
%dir %{_sysconfdir}/ppp/rp-pppoe-gui
%{_datadir}/tkpppoe/*

%files plugin
%doc doc/KERNEL-MODE-PPPOE
%attr(755,root,root) %{_libdir}/pppd/%{pppver}/rp-pppoe.so
