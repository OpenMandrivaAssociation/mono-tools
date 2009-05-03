 %define name mono-tools
%define version 2.4
%define release %mkrel 1
%define monodir %_prefix/lib/mono
%define monodocdir %_prefix/lib/monodoc
%define monover 2.4
%define pkgconfigdir %_datadir/pkgconfig
Summary: Mono tools, including the documentation browser
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://go-mono.com/sources/mono-tools/%{name}-%{version}.tar.bz2
License: GPLv2 and LGPLv2
Group: Development/Other
Url: http://www.go-mono.com
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
#gw it needs System.Xml.Linq:
BuildRequires: mono-devel >= %monover
BuildRequires: gnome-sharp2-devel
BuildRequires: gnome-desktop-sharp-devel
BuildRequires: glade-sharp2
BuildRequires: webkit-sharp-devel
Requires(post): monodoc-core >= %monover
Requires: monodoc-core >= %monover
BuildArch: noarch

%description
Mono Tools is a collection of development and testing programs and
utilities for use with Mono.

%prep
%setup -q

%build
./configure --prefix=%_prefix --libdir=%_prefix/lib --mandir=%_mandir
#gw parallel make fails in 2.2
make

%install
rm -rf $RPM_BUILD_ROOT %name.lang
%makeinstall_std pkgconfigdir=%pkgconfigdir
%find_lang %name

touch %buildroot%monodocdir/monodoc.index

%post
%if %mdkversion < 200900
%update_menus
%endif
touch %monodocdir/monodoc.index
%_bindir/monodoc --make-index > /dev/null

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS README ChangeLog
%_bindir/monodoc
%_bindir/mperfmon
%_bindir/gasnview
%_bindir/gendarme
%_bindir/gendarme-wizard
%_bindir/gsharp
%_bindir/gui-compare
%_bindir/create-native-map
%_bindir/ilcontrast
%_bindir/mprof*
%_prefix/lib/create-native-map
%_prefix/lib/ilcontrast/
%dir %_prefix/lib/%name
%_prefix/lib/%name/mprof*
%_mandir/man1/*
%_prefix/lib/gendarme
%_prefix/lib/gsharp
%_prefix/lib/gui-compare
%_prefix/lib/mperfmon
%monodir/1.0/*
%monodocdir/browser.exe
%monodocdir/GtkHtmlHtmlRender.dll
%monodocdir/MonoWebBrowserHtmlRender.dll
%monodocdir/WebKitHtmlRender.dll
%monodocdir/sources/Gendarme*
%monodocdir/sources/gendarme*
%pkgconfigdir/*.pc
%_datadir/applications/gendarme-wizard.desktop
%_datadir/applications/gsharp.desktop
%_datadir/applications/monodoc.desktop
%_datadir/applications/mprof-heap-viewer.desktop
%_datadir/applications/ilcontrast.desktop
%_datadir/pixmaps/*
%ghost %monodocdir/monodoc.index


