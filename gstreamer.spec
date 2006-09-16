
%define		_vmajor		0.10
%define		_vminor		10

Summary:	GStreamer Streaming-media framework runtime
Summary(pl):	GStreamer - biblioteki ¶rodowiska do obróbki strumieni
Name:		gstreamer
Version:	%{_vmajor}.%{_vminor}
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://gstreamer.freedesktop.org/src/gstreamer/%{name}-%{version}.tar.bz2
# Source0-md5:	6875bf0bd3cf38b9ae1362b9e644e6fc
Patch0:		%{name}-without_ps_pdf.patch
Patch1:		%{name}-eps.patch
URL:		http://gstreamer.net/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1.6
BuildRequires:	bison >= 1.35
BuildRequires:	check >= 0.9.3-2
BuildRequires:	docbook-utils >= 0.6.10
BuildRequires:	flex
BuildRequires:	glib2-devel >= 1:2.12.0
BuildRequires:	gtk-doc >= 1.6
BuildRequires:	libtool >= 1.4
BuildRequires:	libxml2-devel >= 1:2.6.26
BuildRequires:	nasm
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	popt-devel >= 1.6.3
# not sure it is a right place for this BR
BuildRequires:	python-PyXML
BuildRequires:	transfig
BuildRequires:	xmlto
Requires:	glib2 >= 1:2.12.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_gstlibdir	%{_libdir}/gstreamer-%{_vmajor}
%define		_gstincludedir	%{_includedir}/gstreamer-%{_vmajor}

%description
GStreamer is a streaming-media framework, based on graphs of filters
which operate on media data. Applications using this library can do
anything from real-time sound processing to playing videos, and just
about anything else media-related. Its plugin-based architecture means
that new data types or processing capabilities can be added simply by
installing new plugins.

%description -l pl
GStreamer to ¶rodowisko obróbki danych strumieniowych, bazuj±ce na
grafie filtrów operuj±cych na danych medialnych. Aplikacje u¿ywaj±ce
tej biblioteki mog± robiæ wszystko od przetwarzania d¼wiêku w czasie
rzeczywistym, do odtwarzania filmów i czegokolwiek innego zwi±zanego z
mediami. Architektura bazuj±ca na wtyczkach pozwala na ³atwe dodawanie
nowych typów danych lub mo¿liwo¶ci obróbki.

%package devel
Summary:	Include files for GStreamer streaming-media framework
Summary(pl):	Pliki nag³ówkowe do ¶rodowiska obróbki strumieni GStreamer
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.12.0
Requires:	libxml2-devel >= 1:2.6.26
Requires:	popt-devel >= 1.6.3

%description devel
This package contains the includes files necessary to develop
applications and plugins for GStreamer.

%description devel -l pl
Ten pakiet zawiera pliki nag³ówkowe potrzebne do rozwijania aplikacji
i wtyczek do GStreamera.

%package static
Summary:	GStreamer static libraries
Summary(pl):	Biblioteki statyczne GStreamer
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static versions of GStreamer libraries.

%description static -l pl
Statyczne wersje bibliotek GStreamer.

%package apidocs
Summary:	GStreamer API documentation
Summary(pl):	Dokumentacja API Gstreamera
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
GStreamer API documentation.

%description apidocs -l pl
Dokumentacja API Gstreamera.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I common/m4
%{__autoconf}
%{__autoheader}
%{__automake}
LDFLAGS="%{rpmldflags} -Wl,--as-needed"
%configure \
	--disable-examples \
	--disable-pspdf \
	--disable-tests \
	--enable-docbook \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_docdir}/%{name}-devel-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_docdir}/%{name}-{%{_vmajor},%{version}}
mv $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/{manual,pwg} \
	$RPM_BUILD_ROOT%{_docdir}/%{name}-devel-%{version}

%find_lang %{name} --all-name --with-gnome

# no static modules and *.la for them - shut up check files
rm -f $RPM_BUILD_ROOT%{_gstlibdir}/lib*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%dir %{_gstlibdir}
%attr(755,root,root) %{_gstlibdir}/*.so
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_docdir}/%{name}-devel-%{version}
%{_gstincludedir}
%{_pkgconfigdir}/*
%{_aclocaldir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/*
