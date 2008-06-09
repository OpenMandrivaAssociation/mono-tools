 %define name mono-tools
%define version 1.9
%define release %mkrel 1
%define monodir %_prefix/lib/mono
%define monodocdir %_prefix/lib/monodoc
%define monodocver 1.1.9
%define pkgconfigdir %_datadir/pkgconfig
Summary: Mono tools, including the documentation browser
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://go-mono.com/sources/mono-tools/%{name}-%{version}.tar.bz2
Patch: mono-tools-firefox.patch
License: GPL/LGPL
Group: Development/Other
Url: http://www.go-mono.com
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: mono-devel >= 1.9
BuildRequires: monodoc >= %monodocver
BuildRequires: gnome-sharp2-devel
BuildRequires: gnome-desktop-sharp-devel
BuildRequires: glade-sharp2
BuildRequires: gecko-sharp2
BuildRequires: ImageMagick
BuildRequires: desktop-file-utils
Requires(post): monodoc >= %monodocver
Requires: monodoc >= %monodocver
Requires: mozilla-firefox
BuildArch: noarch

%description
Mono Tools is a collection of development and testing programs and
utilities for use with Mono.

%prep
%setup -q
%patch -p1 -b .firefox

%build
./configure --prefix=%_prefix --libdir=%_prefix/lib --mandir=%_mandir
%make

%install
rm -rf $RPM_BUILD_ROOT %name.lang
%makeinstall_std pkgconfigdir=%pkgconfigdir
%find_lang %name
#menu
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-MoreApplications-Documentation" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/monodoc.desktop
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-MoreApplications-Development-Tools" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/ilcontrast.desktop


mkdir -p %buildroot{%_liconsdir,%_miconsdir,%_iconsdir}
ln -s %_datadir/pixmaps/monodoc.png %buildroot/%_liconsdir/monodoc.png
convert -scale 32x32 %buildroot%_datadir/pixmaps/monodoc.png %buildroot%{_iconsdir}/monodoc.png
convert -scale 16x16 %buildroot%_datadir/pixmaps/monodoc.png %buildroot%{_miconsdir}/monodoc.png

touch %buildroot%monodocdir/monodoc.index

%post
%update_menus
touch %monodocdir/monodoc.index
%_bindir/monodoc --make-index > /dev/null

%postun
%clean_menus

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS README ChangeLog
%_bindir/monodoc
%_bindir/gasnview
%_bindir/gendarme
%_bindir/gnunit
%_bindir/gnunit2
%_bindir/gui-compare
%_bindir/create-native-map
%_bindir/ilcontrast
%_prefix/lib/create-native-map
%_prefix/lib/ilcontrast/
%_mandir/man1/*
%_prefix/lib/gendarme
%_prefix/lib/gui-compare
%monodir/1.0/*
%monodir/2.0/*
%monodocdir/browser.exe
%monodocdir/GeckoHtmlRender.dll
%monodocdir/GtkHtmlHtmlRender.dll
%pkgconfigdir/*.pc
%_datadir/pixmaps/monodoc.png
%_datadir/pixmaps/ilcontrast.png
%_datadir/applications/monodoc.desktop
%_datadir/applications/ilcontrast.desktop
%_liconsdir/monodoc.png
%_iconsdir/monodoc.png
%_miconsdir/monodoc.png
%ghost %monodocdir/monodoc.index


