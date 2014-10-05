#
%define		vmajor		1.0
#
Summary:	GStreamer Streaming-media framework runtime
Summary(pl.UTF-8):	GStreamer - biblioteki środowiska do obróbki strumieni
Name:		gstreamer
Version:	1.4.3
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://gstreamer.freedesktop.org/src/gstreamer/%{name}-%{version}.tar.xz
# Source0-md5:	7934fd965bbe1398f0ff1edeb7f1fd89
Patch0:		%{name}-without_ps_pdf.patch
Patch1:		%{name}-eps.patch
Patch2:		%{name}-inspect-rpm-format.patch
URL:		http://gstreamer.net/
BuildRequires:	autoconf >= 2.68
BuildRequires:	automake >= 1:1.11
BuildRequires:	bison >= 1.875
BuildRequires:	docbook-dtd30-sgml
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-utils >= 0.6.10
BuildRequires:	flex >= 2.5.31
BuildRequires:	gettext-devel >= 0.17
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	glibc-misc
BuildRequires:	gnome-doc-tools
BuildRequires:	gobject-introspection-devel >= 1.31.1
BuildRequires:	gtk-doc >= 1.12
BuildRequires:	libtool >= 1.4
BuildRequires:	nasm
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	python >= 2.1
BuildRequires:	tar >= 1:1.22
BuildRequires:	transfig
BuildRequires:	xmlto
BuildRequires:	xz
Requires:	glib2 >= 1:2.32.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_gstlibdir	%{_libdir}/gstreamer-%{vmajor}
%define		_gstincludedir	%{_includedir}/gstreamer-%{vmajor}

%description
GStreamer is a streaming-media framework, based on graphs of filters
which operate on media data. Applications using this library can do
anything from real-time sound processing to playing videos, and just
about anything else media-related. Its plugin-based architecture means
that new data types or processing capabilities can be added simply by
installing new plugins.

%description -l pl.UTF-8
GStreamer to środowisko obróbki danych strumieniowych, bazujące na
grafie filtrów operujących na danych medialnych. Aplikacje używające
tej biblioteki mogą robić wszystko od przetwarzania dźwięku w czasie
rzeczywistym, do odtwarzania filmów i czegokolwiek innego związanego z
mediami. Architektura bazująca na wtyczkach pozwala na łatwe dodawanie
nowych typów danych lub możliwości obróbki.

%package devel
Summary:	Include files for GStreamer streaming-media framework
Summary(pl.UTF-8):	Pliki nagłówkowe do środowiska obróbki strumieni GStreamer
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.32.0
Obsoletes:	gstreamer-plugins-bad-devel < 0.10.10

%description devel
This package contains the includes files necessary to develop
applications and plugins for GStreamer.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do rozwijania aplikacji
i wtyczek do GStreamera.

%package static
Summary:	GStreamer static libraries
Summary(pl.UTF-8):	Biblioteki statyczne GStreamer
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static versions of GStreamer libraries.

%description static -l pl.UTF-8
Statyczne wersje bibliotek GStreamer.

%package apidocs
Summary:	GStreamer API documentation
Summary(pl.UTF-8):	Dokumentacja API Gstreamera
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
GStreamer API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API Gstreamera.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
# po/Makefile.in.in is modified
#{__gettextize}
%{__libtoolize}
%{__aclocal} -I common/m4 -I m4 -I .
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-examples \
	--disable-pspdf \
	--disable-silent-rules \
	--disable-tests \
	--enable-docbook \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir} \
	--enable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_docdir}/%{name}-devel-%{version},%{rpmlibdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_docdir}/%{name}-{%{vmajor},%{version}}
mv $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/{faq,manual,pwg} \
	$RPM_BUILD_ROOT%{_docdir}/%{name}-devel-%{version}

%find_lang %{name} --all-name --with-gnome

# no *.la for modules - shut up check files
%{__rm} $RPM_BUILD_ROOT%{_gstlibdir}/lib*.la
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgst*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog MAINTAINERS NEWS README RELEASE
%attr(755,root,root) %{_bindir}/gst-inspect-1.0
%attr(755,root,root) %{_bindir}/gst-launch-1.0
%attr(755,root,root) %{_bindir}/gst-typefind-1.0
%attr(755,root,root) %{_libdir}/libgstbase-%{vmajor}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstbase-%{vmajor}.so.0
%attr(755,root,root) %{_libdir}/libgstcheck-%{vmajor}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstcheck-%{vmajor}.so.0
%attr(755,root,root) %{_libdir}/libgstcontroller-%{vmajor}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstcontroller-%{vmajor}.so.0
%attr(755,root,root) %{_libdir}/libgstnet-%{vmajor}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstnet-%{vmajor}.so.0
%attr(755,root,root) %{_libdir}/libgstreamer-%{vmajor}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstreamer-%{vmajor}.so.0
%dir %{_gstlibdir}
%attr(755,root,root) %{_gstlibdir}/gst-plugin-scanner
%attr(755,root,root) %{_gstlibdir}/libgstcoreelements.so
%{_mandir}/man1/gst-inspect-1.0.1*
%{_mandir}/man1/gst-launch-1.0.1*
%{_mandir}/man1/gst-typefind-1.0.1*
%{_libdir}/girepository-1.0/Gst-%{vmajor}.typelib
%{_libdir}/girepository-1.0/GstBase-%{vmajor}.typelib
%{_libdir}/girepository-1.0/GstCheck-%{vmajor}.typelib
%{_libdir}/girepository-1.0/GstController-%{vmajor}.typelib
%{_libdir}/girepository-1.0/GstNet-%{vmajor}.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgstbase-%{vmajor}.so
%attr(755,root,root) %{_libdir}/libgstcheck-%{vmajor}.so
%attr(755,root,root) %{_libdir}/libgstcontroller-%{vmajor}.so
%attr(755,root,root) %{_libdir}/libgstnet-%{vmajor}.so
%attr(755,root,root) %{_libdir}/libgstreamer-%{vmajor}.so
%{_docdir}/%{name}-devel-%{version}
%{_gstincludedir}
%{_pkgconfigdir}/gstreamer-%{vmajor}.pc
%{_pkgconfigdir}/gstreamer-base-%{vmajor}.pc
%{_pkgconfigdir}/gstreamer-check-%{vmajor}.pc
%{_pkgconfigdir}/gstreamer-controller-%{vmajor}.pc
%{_pkgconfigdir}/gstreamer-net-%{vmajor}.pc
%{_aclocaldir}/gst-element-check-%{vmajor}.m4
%{_datadir}/gir-1.0/Gst-%{vmajor}.gir
%{_datadir}/gir-1.0/GstBase-%{vmajor}.gir
%{_datadir}/gir-1.0/GstCheck-%{vmajor}.gir
%{_datadir}/gir-1.0/GstController-%{vmajor}.gir
%{_datadir}/gir-1.0/GstNet-%{vmajor}.gir

%files static
%defattr(644,root,root,755)
%{_libdir}/libgstbase-%{vmajor}.a
%{_libdir}/libgstcheck-%{vmajor}.a
%{_libdir}/libgstcontroller-%{vmajor}.a
%{_libdir}/libgstnet-%{vmajor}.a
%{_libdir}/libgstreamer-%{vmajor}.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gstreamer-%{vmajor}
%{_gtkdocdir}/gstreamer-libs-%{vmajor}
%{_gtkdocdir}/gstreamer-plugins-%{vmajor}
