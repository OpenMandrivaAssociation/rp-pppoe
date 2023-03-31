%define	pppver	2.4.7

Summary:	ADSL/PPPoE userspace driver
Name:		rp-pppoe
Version:	3.15
Release:	2
License:	GPLv2+
Group:		System/Servers
Url:		http://www.roaringpenguin.com/products/pppoe
Source0:	https://dianne.skoll.ca/projects/rp-pppoe/download/%{name}-%{version}.tar.gz
Source3:	http://www.luigisgro.com/sw/rp-pppoe-3.8.patch/README-first-session-packet-lost.txt
Source4:	pppoe-server.service
Source5:	pppoe.service
Patch0:		rp-pppoe-3.8-CAN-2004-0564.patch
Patch1:		rp-pppoe-3.11-override-incompatible-compiler-and-linker-flags.patch
Patch2:		rp-pppoe-3.10-lsb.patch
Patch3:		pass-cflags-to-wrapper.patch
BuildRequires:	ppp-devel 
Requires:	ppp >= 2.4.1

%description
PPPoE (Point-to-Point Protocol over Ethernet) is a protocol used by
many ADSL Internet Service Providers. Roaring Penguin has a free
client for Linux systems to connect to PPPoE service providers.

The client is a user-mode program and does not require any kernel
modifications. It is fully compliant with RFC 2516, the official PPPoE
specification.

It has been tested with many ISPs, such as the Canadian Sympatico HSE (High
Speed Edition) service.

%package	gui
Summary:	GUI front-end for rp-pppoe
Group:		System/Servers
Requires:	rp-pppoe >= 3.6
Requires:	tk

%description	gui
This package contains the graphical frontend (tk-based) for rp-pppoe.

Install this if you wish to have a graphical frontend for pppoe.

%prep
%setup -q
%autopatch -p1
cp %{SOURCE3} ./README-first-session-packet-lost.txt

%build
%serverbuild
cd src
%configure \
	--docdir=%{_docdir}/%{name} \
	--disable-plugin

%make_build

%install
%make_install -C src

LDFLAGS="%{ldflags}" %make_install -C gui

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

rm -f %{buildroot}%{_initrddir}/pppoe
install -D -m 0644 %{SOURCE4} %{buildroot}%{_unitdir}/pppoe-server.service
install -D -m 0644 %{SOURCE5} %{buildroot}%{_unitdir}/pppoe.service

rm -r %{buildroot}%{_sysconfdir}/ppp/plugins

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
%doc %{_mandir}/man[58]/*
%{_unitdir}/pppoe-server.service
%{_unitdir}/pppoe.service

%files gui
%{_bindir}/tkpppoe
%{_sbindir}/pppoe-wrapper
%doc %{_mandir}/man1/*
%{_datadir}/applications/*
%dir %{_datadir}/tkpppoe
%dir %{_sysconfdir}/ppp/rp-pppoe-gui
%{_datadir}/tkpppoe/*
