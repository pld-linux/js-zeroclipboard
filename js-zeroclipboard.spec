%define		pkgname	zeroclipboard
Summary:	Copy to clipboard HTML browser
Name:		js-%{pkgname}
Version:	2.2.0
Release:	2
License:	MIT
Group:		Applications/WWW
Source0:	https://github.com/zeroclipboard/zeroclipboard/archive/v%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	74be02c6583a27abae640f4ddecc60b5
Source1:	apache.conf
Source2:	lighttpd.conf
URL:		http://zeroclipboard.org/
BuildRequires:	rpmbuild(macros) >= 1.553
BuildRequires:	sed >= 4.0
Requires:	webserver(access)
Requires:	webserver(alias)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
The ZeroClipboard library provides an easy way to copy text to the
clipboard using an invisible Adobe Flash movie and a JavaScript
interface.

The "Zero" signifies that the library is invisible and the user
interface is left entirely up to you.

%prep
%setup -qn %{pkgname}-%{version}
mv dist/ZeroClipboard{,.src}.js
%{__sed} -i -e '/# sourceMappingURL=/d' dist/ZeroClipboard.min.js

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}
cp -a dist/* $RPM_BUILD_ROOT%{_appdir}
ln -s ZeroClipboard.min.js $RPM_BUILD_ROOT%{_appdir}/ZeroClipboard.js

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
cp -p $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc README.md CONTRIBUTING.md LICENSE docs/*.md
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%dir %{_appdir}
%{_appdir}/ZeroClipboard*.js
%{_appdir}/ZeroClipboard*.min.map
%{_appdir}/ZeroClipboard.swf
