#
# spec file for package opsi-atftp
#
# Copyright (c) 2008 uib GmbH.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:           opsi-atftp
Requires:       xinetd
License:        GPL v2 or later
Group:          Productivity/Networking/Opsi
AutoReqProv:    on
Version:        0.7
Release:        1
Conflicts:      atftp
Summary:        advanced TFTP server - opsi version with pcre, fifo and max-blksize patches
%define tarname opsi-atftp
Source:         %{tarname}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

# ===[ description ]================================
%description
Multi-threaded TFTP server implementing all options (option extension and
multicast) as specified in RFC1350, RFC2090, RFC2347, RFC2348 and RFC2349.
Atftpd also supports multicast protocol known as mtftp, defined in the PXE
specification. The server is started from xinetd(8).
This version of atftpd is patched to support reading from named pipes and
blksize limits.

%package client
Summary: Advanced Trivial File Transfer Protocol (ATFTP) - TFTP client
Group: Applications/Internet

%description client
Advanced Trivial File Transfer Protocol client program for requesting
files using the TFTP protocol.

# ===[ debug_package ]==============================
%debug_package

# ===[ prep ]=======================================
%prep

# ===[ setup ]======================================
%setup

# ===[ patch ]======================================
%patch

%{__cat} <<EOF >tftp.xinetd
service tftp
{
    disable         = no
    socket_type     = dgram
    protocol        = udp
    wait            = yes
    user            = root
    server          = %{_sbindir}/in.tftpd
    server_args     = /tftpboot
    per_source      = 11
    cps             = 100 2
    flags           = IPv4
}
EOF

# ===[ build ]======================================
%build
%configure
make

# ===[ install ]====================================
%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != '/' ] && rm -rf $RPM_BUILD_ROOT
%makeinstall
install -Dp -m0644 tftp.xinetd %{buildroot}%{_sysconfdir}/xinetd.d/tftp

# ===[ clean ]======================================
%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != '/' ] && rm -rf $RPM_BUILD_ROOT

# ===[ post ]=======================================
%post

# ===[ preun ]======================================
%preun
%stop_on_removal opsipxeconfd

# ===[ postun ]=====================================
%postun
%restart_on_update opsipxeconfd
%insserv_cleanup

# ===[ files ]======================================
%files
%{_mandir}/man8/atftpd.8.gz
%{_sbindir}/atftpd
%{_mandir}/man8/in.tftpd.8.gz
%{_sbindir}/in.tftpd
%config(noreplace) %{_sysconfdir}/xinetd.d/tftp

%files client
%{_mandir}/man1/atftp.1.gz
%{_bindir}/atftp

# ===[ changelog ]==================================
%changelog
* Fri Sep 19 2008 - j.schneider@uib.de
- created new package

