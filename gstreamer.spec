Summary:	GStreamer Streaming-media framework runtime
Summary(pl.UTF-8):	GStreamer - biblioteki środowiska do obróbki strumieni
Name:		gstreamer
Version:	0.10.28
Release:	2
License:	LGPL v2+
Group:		Libraries
Source0:	http://gstreamer.freedesktop.org/src/gstreamer/%{name}-%{version}.tar.bz2
# Source0-md5:	1c7accac718fe211ff91323c27d4ae02
Source1:	%{name}-rpmdeps.sh
Patch0:		%{name}-without_ps_pdf.patch
Patch1:		%{name}-eps.patch
Patch2:		%{name}-inspect-rpm-format.patch
URL:		http://gstreamer.net/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1.6
BuildRequires:	bison >= 1.35
BuildRequires:	check >= 0.9.3-2
BuildRequires:	docbook-dtd30-sgml
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-utils >= 0.6.10
BuildRequires:	flex
BuildRequires:	gettext-devel >= 0.11.5
BuildRequires:	glib2-devel >= 1:2.18.0
BuildRequires:	glibc-misc
BuildRequires:	gnome-doc-tools
BuildRequires:	gobject-introspection-devel >= 0.6.5
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
Requires:	glib2 >= 1:2.18.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		vmajor		%(echo %{version} | cut -d. -f1,2)
%define		_gstlibdir	%{_libdir}/gstreamer-%{vmajor}
%define		_gstincludedir	%{_includedir}/gstreamer-%{vmajor}

%define		rpmlibdir	/usr/lib/rpm

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
Requires:	glib2-devel >= 1:2.18.0
Requires:	libxml2-devel >= 1:2.6.26
Requires:	popt-devel >= 1.6.3
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
%{__aclocal} -I common/m4 -I .
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-examples \
	--disable-pspdf \
	--disable-tests \
	--enable-docbook \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}

%{__make} V=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_docdir}/%{name}-devel-%{version},%{rpmlibdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{rpmlibdir}/gstreamerdeps.sh

mv $RPM_BUILD_ROOT%{_docdir}/%{name}-{%{vmajor},%{version}}
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
%attr(755,root,root) %{_bindir}/gst-*
%attr(755,root,root) %{_libdir}/libgstbase-0.10.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstbase-0.10.so.0
%attr(755,root,root) %{_libdir}/libgstcheck-0.10.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstcheck-0.10.so.0
%attr(755,root,root) %{_libdir}/libgstcontroller-0.10.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstcontroller-0.10.so.0
%attr(755,root,root) %{_libdir}/libgstdataprotocol-0.10.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstdataprotocol-0.10.so.0
%attr(755,root,root) %{_libdir}/libgstnet-0.10.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstnet-0.10.so.0
%attr(755,root,root) %{_libdir}/libgstreamer-0.10.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstreamer-0.10.so.0
%dir %{_gstlibdir}
%attr(755,root,root) %{_gstlibdir}/gst-plugin-scanner
%attr(755,root,root) %{_gstlibdir}/libgstcoreelements.so
%attr(755,root,root) %{_gstlibdir}/libgstcoreindexers.so
%{_mandir}/man1/gst-*.1*
%{_libdir}/girepository-1.0/Gst-0.10.typelib
%{_libdir}/girepository-1.0/GstBase-0.10.typelib
%{_libdir}/girepository-1.0/GstCheck-0.10.typelib
%{_libdir}/girepository-1.0/GstController-0.10.typelib
%{_libdir}/girepository-1.0/GstNet-0.10.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgstbase-0.10.so
%attr(755,root,root) %{_libdir}/libgstcheck-0.10.so
%attr(755,root,root) %{_libdir}/libgstcontroller-0.10.so
%attr(755,root,root) %{_libdir}/libgstdataprotocol-0.10.so
%attr(755,root,root) %{_libdir}/libgstnet-0.10.so
%attr(755,root,root) %{_libdir}/libgstreamer-0.10.so
%{_libdir}/libgstbase-0.10.la
%{_libdir}/libgstcheck-0.10.la
%{_libdir}/libgstcontroller-0.10.la
%{_libdir}/libgstdataprotocol-0.10.la
%{_libdir}/libgstnet-0.10.la
%{_libdir}/libgstreamer-0.10.la
%{_docdir}/%{name}-devel-%{version}
%{_gstincludedir}
%{_pkgconfigdir}/gstreamer-0.10.pc
%{_pkgconfigdir}/gstreamer-base-0.10.pc
%{_pkgconfigdir}/gstreamer-check-0.10.pc
%{_pkgconfigdir}/gstreamer-controller-0.10.pc
%{_pkgconfigdir}/gstreamer-dataprotocol-0.10.pc
%{_pkgconfigdir}/gstreamer-net-0.10.pc
%{_aclocaldir}/gst-element-check-0.10.m4
%attr(755,root,root) %{rpmlibdir}/gstreamerdeps.sh
%{_datadir}/gir-1.0/Gst-0.10.gir
%{_datadir}/gir-1.0/GstBase-0.10.gir
%{_datadir}/gir-1.0/GstCheck-0.10.gir
%{_datadir}/gir-1.0/GstController-0.10.gir
%{_datadir}/gir-1.0/GstNet-0.10.gir

%files static
%defattr(644,root,root,755)
%{_libdir}/libgstbase-0.10.a
%{_libdir}/libgstcheck-0.10.a
%{_libdir}/libgstcontroller-0.10.a
%{_libdir}/libgstdataprotocol-0.10.a
%{_libdir}/libgstnet-0.10.a
%{_libdir}/libgstreamer-0.10.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gstreamer-0.10
%{_gtkdocdir}/gstreamer-libs-0.10
%{_gtkdocdir}/gstreamer-plugins-0.10
