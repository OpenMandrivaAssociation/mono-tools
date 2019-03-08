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
Source1:        gsharp.svg
Patch1:         mono-tools-2.11-disable-gendarme-webdoc-build.patch
Patch2:         gsharp_icon.patch
Patch3:         mono-tools-4.2-docbrowser.patch
BuildArch:	noarch
BuildRequires:	pkgconfig(glade-sharp-2.0)
BuildRequires:	pkgconfig(mono) >= %{monover}
BuildRequires:	pkgconfig(webkit-sharp-1.0)
#BuildRequires:	pkgconfig(mono-nunit)
BuildRequires:	pkgconfig(nunit22)
BuildRequires:	zip
Requires(post):	monodoc-core >= %{monover}
Requires:	monodoc-core >= %{monover}

%description
Mono Tools is a collection of development and testing programs and
utilities for use with Mono.

%prep
%setup -q
%patch1 -p1 -b .disable_gendarme
%patch2 -p0 -b .gsharp_icon
%patch3 -p1 -b .docbrowser

for i in `find . -name "*.am"`;
do
	sed -i -e 's|-define:DEBUG|-define:DEBUG -sdk:4|g' $i
done

find . -name "Makefile.in" -print -exec sed -i "s#GMCS#MCS#g; s#DMCS#MCS#g" {} \;
find . -name "configure" -print -exec sed -i "s#GMCS#MCS#g; s#DMCS#MCS#g" {} \;
sed -i "s#mono-nunit#nunit#g" configure
sed -i "s#mono-nunit#nunit#g" gendarme/rules/Test.Rules/Makefile.in

%build
%configure2_5x --libdir=%{_prefix}/lib --build=%{_build}
#gw parallel make fails in 2.2
%__make

%install
%make_install pkgconfigdir=%pkgconfigdir

%find_lang %name

#gw it needs Mono.WebBrowser which needs gluezilla
rm -f %buildroot%monodocdir/MonoWebBrowserHtmlRender.dll
touch %buildroot%monodocdir/monodoc.index

mkdir -p %buildroot%_iconsdir
cp %{SOURCE1} %buildroot%_iconsdir

%files -f %name.lang
%doc AUTHORS README ChangeLog
%_bindir/emveepee
%_bindir/minvoke
%_bindir/monodoc
%_bindir/mperfmon
%_bindir/gasnview
%_bindir/gd2i
%_bindir/gendarme
%_bindir/gendarme-wizard
%_bindir/gsharp
%_bindir/gui-compare
%_bindir/create-native-map
%_bindir/mprof*
%_prefix/lib/create-native-map
%dir %_prefix/lib/minvoke/
%_prefix/lib/minvoke/minvoke.exe
%dir %_prefix/lib/%name
%_prefix/lib/%name/emveepee.exe*
%_prefix/lib/%name/mprof*
%_prefix/lib/%name/Mono.Profiler*
%_mandir/man1/*
%_mandir/man5/*
%_prefix/lib/gendarme
%_prefix/lib/gsharp
%_prefix/lib/gui-compare
%_prefix/lib/mperfmon
%_iconsdir/gsharp.*
%monodir/1.0/*
%monodocdir/browser.exe
%monodocdir/sources/Gendarme*
%monodocdir/sources/gendarme*
%monodocdir/web
%pkgconfigdir/*.pc
%_datadir/applications/gendarme-wizard.desktop
%_datadir/applications/gsharp.desktop
%_datadir/applications/monodoc.desktop
%_datadir/pixmaps/*
%_datadir/icons/hicolor/*/apps/*
%ghost %monodocdir/monodoc.index

