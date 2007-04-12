 %define name mono-tools
%define version 1.2.3
%define release %mkrel 1
%define monodir %_prefix/lib/mono
%define monodocdir %_prefix/lib/monodoc
%define monodocver 1.1.9
%if %mdkversion >= 200600
%define pkgconfigdir %_datadir/pkgconfig
%else
%define pkgconfigdir %_libdir/pkgconfig
%endif
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
BuildRequires: mono-devel
BuildRequires: monodoc >= %monodocver
BuildRequires: gnome-sharp2
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
install -d -m 755 $RPM_BUILD_ROOT%{_menudir}
cat >$RPM_BUILD_ROOT%{_menudir}/%{name} <<EOF
?package(%{name}): \
	command="%{_bindir}/monodoc" \
	needs="X11" \
	section="More Applications/Documentation" \
	icon="monodoc.png" \
	title="Monodoc" \
	longtitle="Monodoc Documentation Browser" \
	startup_notify="false" xdg="true"
EOF
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-MoreApplications-Documentation" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

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
%_bindir/gnunit
%_bindir/gnunit2
%_bindir/create-native-map
%_prefix/lib/create-native-map
%_mandir/man1/*
%monodir/1.0/*
%monodir/2.0/*
%monodocdir/browser.exe
%monodocdir/GeckoHtmlRender.dll
%monodocdir/GtkHtmlHtmlRender.dll
%pkgconfigdir/*.pc
%_datadir/pixmaps/monodoc.png
%_datadir/applications/monodoc.desktop
%_menudir/%name
%_liconsdir/monodoc.png
%_iconsdir/monodoc.png
%_miconsdir/monodoc.png
%ghost %monodocdir/monodoc.index


