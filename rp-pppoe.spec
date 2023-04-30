%define	pppver	2.4.7

Summary:	ADSL/PPPoE userspace driver
Name:		rp-pppoe
Version:	4.0
Release:	1
License:	GPLv2+
Group:		System/Servers
Url:		http://www.roaringpenguin.com/products/pppoe
Source0:	https://dianne.skoll.ca/projects/rp-pppoe/download/rp-pppoe-%{version}.tar.gz
Source3:	http://www.luigisgro.com/sw/rp-pppoe-3.8.patch/README-first-session-packet-lost.txt
Source4:	pppoe-server.service
Source5:	pppoe.service
Patch0:		rp-pppoe-3.8-CAN-2004-0564.patch
Patch1:		rp-pppoe-3.11-override-incompatible-compiler-and-linker-flags.patch
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

%prep
%setup -q
%autopatch -p1
cp %{SOURCE3} ./README-first-session-packet-lost.txt

%build
%serverbuild
cd src
%configure \
	--docdir=%{_docdir}/%{name}

%make_build

%install
%make_install -C src

rm -f %{buildroot}%{_initrddir}/pppoe
install -D -m 0644 %{SOURCE4} %{buildroot}%{_unitdir}/pppoe-server.service
install -D -m 0644 %{SOURCE5} %{buildroot}%{_unitdir}/pppoe.service

rm -r %{buildroot}%{_sysconfdir}/ppp/plugins

%files
%doc README-first-session-packet-lost.txt
%doc %{_docdir}/%{name}-%{version}/*
%config(noreplace) %{_sysconfdir}/ppp/pppoe-server-options
%{_sbindir}/pppoe
%{_sbindir}/pppoe-relay
%{_sbindir}/pppoe-server
%{_sbindir}/pppoe-sniff
%doc %{_mandir}/man[58]/*
%{_unitdir}/pppoe-server.service
%{_unitdir}/pppoe.service
