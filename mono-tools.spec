%if %{_use_internal_dependency_generator}
%define __noautoreq 'lib\.*gtk'
%else
%define _requires_exceptions lib.*gtk
%endif

%define monodir %{_prefix}/lib/mono
%define monodocdir %{_prefix}/lib/monodoc
%define monover 2.10
%define pkgconfigdir %{_datadir}/pkgconfig

Summary:	Mono tools, including the documentation browser
Name:		mono-tools
Version:	4.2
Release:	4
License:	GPLv2 and LGPLv2
Group:		Development/Other
Url:		http://www.go-mono.com
Source0:	http://download.mono-project.com/sources/%{name}/%{name}-%{version}.tar.gz
Source100:	mono-tools.rpmlintrc
BuildArch:	noarch
BuildRequires:	pkgconfig(glade-sharp-2.0)
BuildRequires:	pkgconfig(mono) >= %{monover}
BuildRequires:	pkgconfig(webkit-sharp-1.0)
BuildRequires:	pkgconfig(mono-nunit)
BuildRequires:	zip
Requires(post):	monodoc-core >= %{monover}
Requires:	monodoc-core >= %{monover}

%description
Mono Tools is a collection of development and testing programs and
utilities for use with Mono.

%prep
%setup -q

%build
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_prefix}/lib \
	--mandir=%{_mandir}
#gw parallel make fails in 2.2
make

%install
%makeinstall_std pkgconfigdir=%{pkgconfigdir}
%find_lang %{name}
#gw it needs Mono.WebBrowser which needs gluezilla
rm -f %{buildroot}%{monodocdir}/MonoWebBrowserHtmlRender.dll
touch %{buildroot}%{monodocdir}/monodoc.index

%post
touch %{monodocdir}/monodoc.index
%{_bindir}/monodoc --make-index > /dev/null

%files -f %{name}.lang
%doc AUTHORS README ChangeLog
%{_bindir}/emveepee
%{_bindir}/minvoke
%{_bindir}/monodoc
%{_bindir}/mperfmon
%{_bindir}/gd2i
%{_bindir}/gendarme
%{_bindir}/gendarme-wizard
%{_bindir}/gsharp
%{_bindir}/gui-compare
%{_bindir}/create-native-map
%{_bindir}/ilcontrast
%{_bindir}/mprof*
%{_prefix}/lib/create-native-map
%{_prefix}/lib/ilcontrast/
%dir %{_prefix}/lib/minvoke/
%{_prefix}/lib/minvoke/minvoke.exe
%dir %{_prefix}/lib/%{name}
%{_prefix}/lib/%{name}/emveepee.exe*
%{_prefix}/lib/%{name}/mprof*
%{_prefix}/lib/%{name}/Mono.Profiler*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_prefix}/lib/gendarme
%{_prefix}/lib/gsharp
%{_prefix}/lib/gui-compare
%{_prefix}/lib/mperfmon
%{monodocdir}/browser.exe
%{monodocdir}/WebKitHtmlRender.dll
%{monodocdir}/sources/Gendarme*
%{monodocdir}/sources/gendarme*
%{monodocdir}/web
%{pkgconfigdir}/*.pc
%{_datadir}/applications/gendarme-wizard.desktop
%{_datadir}/applications/gsharp.desktop
%{_datadir}/applications/monodoc.desktop
%{_datadir}/applications/ilcontrast.desktop
%{_datadir}/pixmaps/*
%ghost %{monodocdir}/monodoc.index

