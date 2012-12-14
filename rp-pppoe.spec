%define	pppver	2.4.5

Summary:	ADSL/PPPoE userspace driver
Name:		rp-pppoe
Version:	3.11
Release:	2
Source0:	http://www.roaringpenguin.com/files/download/%{name}-%{version}.tar.gz
Source3:	http://www.luigisgro.com/sw/rp-pppoe-3.8.patch/README-first-session-packet-lost.txt
Patch0:		rp-pppoe-3.8-CAN-2004-0564.patch
Patch1:		rp-pppoe-3.11-override-incompatible-compiler-and-linker-flags.patch
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
		--disable-plugin
%make

%if %{with uclibc}
%{uclibc_cc} -I. -o pppoe-uclibc pppoe.c if.c debug.c common.c ppp.c discovery.c -lcrypt -lutil -Wall -Wno-deprecated-declarations -DPPPOE_PATH='"/sbin/pppoe"' -DPPPD_PATH='"/sbin/pppd"' -DVERSION='"3.0-stg1"' %{uclibc_cflags} -Os -fwhole-program -flto %{ldflags} -Wl,-O1
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

sed -e "s/restart/restart\|reload/g;" -i %{buildroot}%{_initrddir}/pppoe

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
%{_mandir}/man[58]/*
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

%changelog
* Fri Dec 14 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 3.11-2
- drop kernel plugin, it no longer builds and a working build is already
  shipped in 'ppp-pppoe' package
- fix merging with ROSA package

* Thu May 24 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 3.10-5
+ Revision: 800384
- add version to license
- Add LSB headers to initscripts (mga#5262)
- clean out lotsa old junk
- override incompatible compiler & linker flags (P1)
- enable build of uClibc linked pppoe

* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 3.10-4mdv2011.0
+ Revision: 669432
 mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 3.10-3mdv2011.0
+ Revision: 607372
 rebuild

* Tue Jan 19 2010 Olivier Blin <oblin@mandriva.com> 3.10-2mdv2010.1
+ Revision: 493757
 build for ppp 2.4.5 (thanks pterjan-controlled build bot!)

* Thu May 28 2009 Eugeni Dodonov <eugeni@mandriva.com> 3.10-1mdv2010.0
+ Revision: 380657
 Updated to 3.10.
 Dropped P1, P2 and P3 (merged upstream).
 Cleaned spec.

* Sat Apr 11 2009 Funda Wang <fwang@mandriva.org> 3.8-6mdv2009.1
+ Revision: 366208
 reidff CAN patch

  + Antoine Ginies <aginies@mandriva.com>
    - rebuild

* Thu Jun 12 2008 Pixel <pixel@mandriva.com> 3.8-5mdv2009.0
+ Revision: 218429
 rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Sat Mar 08 2008 Olivier Blin <oblin@mandriva.com> 3.8-5mdv2008.1
+ Revision: 182239
 borrow aligned_u64 definition from linux/types.h (not exported to userspace)
 fix detection of kernel pppoe mode
  (linux/if_pppol2tp.h should include linux/in.h for sockaddr_in struct)
 remove old pppox header copy
 restore BuildRoot

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - drop old menu
    - kill re-definition of %%buildroot on Pixel's request

* Mon Jul 30 2007 Giuseppe Ghibò <ghibo@mandriva.com> 3.8-4mdv2008.0
+ Revision: 56482
 Added Luigi Sgro's Patch3 to speed up initial ADSL connection time to ISP.

* Wed Jul 04 2007 Andreas Hasenack <andreas@mandriva.com> 3.8-3mdv2008.0
+ Revision: 48240
 use serverbuild macro (-fstack-protector-all)
 fix docdir


* Sat Mar 03 2007 Giuseppe Ghibò <ghibo@mandriva.com> 3.8-2mdv2007.0
+ Revision: 131846
 Rebuilt against ppp 2.4.4.
 Rebuilt.
 Import rp-pppoe

* Wed Aug 09 2006 Giuseppe Ghibò <ghibo@mandriva.com> 3.8-1mdv2007.0
 Release 3.8.
 XDG menu.

* Thu Mar 02 2006 Giuseppe Ghibò <ghibo@mandriva.com> 3.7-1mdk
 Release 3.7.
 Removed Patch1, merged upstream.

* Tue Aug 30 2005 Giuseppe Ghibò <ghibo@mandriva.com> 3.6-1mdk
 Release 3.6.
 Re-adapted Patch0 (still needed)?
 Added Patch1 (because option rp_pppoe_dev not supported by pppd).
 Added Patch2 for compiling plugin under glibc 2.3.5.

* Sat Apr 09 2005 Olivier Blin <oblin@mandrakesoft.com> 3.5-5mdk
 from Vincent Danen: security update for CAN-2004-0564

* Tue Jun 08 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 3.5-4mdk
 buildrequires

