# TODO: suid/capabilities for ptp-helper?
%define		vmajor		1.0

Summary:	GStreamer Streaming-media framework runtime
Summary(pl.UTF-8):	GStreamer - biblioteki środowiska do obróbki strumieni
Name:		gstreamer
Version:	1.14.4
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://gstreamer.freedesktop.org/src/gstreamer/%{name}-%{version}.tar.xz
# Source0-md5:	f67fbbc42bd85a0701df119f52fb52bd
Patch0:		%{name}-inspect-rpm-format.patch
URL:		https://gstreamer.freedesktop.org/
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.14
BuildRequires:	bison >= 1.875
BuildRequires:	docbook-dtd412-xml
BuildRequires:	elfutils-devel
BuildRequires:	flex >= 2.5.31
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	glib2-devel >= 1:2.40.0
%if %(locale -a | grep -q '^C\.UTF-8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	glibc-misc
BuildRequires:	gobject-introspection-devel >= 1.31.1
BuildRequires:	gtk-doc >= 1.12
BuildRequires:	libcap-devel
BuildRequires:	libtool >= 2:2.2.6
%ifarch %{ix86} %{x8664} x32 %{arm} hppa ia64 mips ppc ppc64 sh
BuildRequires:	libunwind-devel
%endif
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	python >= 2.1
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.40.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		gstlibdir	%{_libdir}/gstreamer-%{vmajor}
%define		gstlibexecdir	%{_libexecdir}/gstreamer-%{vmajor}
%define		gstincludedir	%{_includedir}/gstreamer-%{vmajor}

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
Requires:	glib2-devel >= 1:2.40.0
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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
GStreamer API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API Gstreamera.

%package -n bash-completion-gstreamer
Summary:	Bash completion for GStreamer utilities
Summary(pl.UTF-8):	Bashowe uzupełnianie parametrów narzędzi GStreamera
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0

%description -n bash-completion-gstreamer
Bash completion for GStreamer utilities: gst-inspect and gst-launch.

%description -n bash-completion-gstreamer
Bashowe uzupełnianie parametrów narzędzi GStreamera: gst-inspect oraz
gst-launch.

%prep
%setup -q
%patch0 -p1

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
	--disable-silent-rules \
	--disable-tests \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir} \
	--enable-static

LC_ALL=C.UTF-8 \
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name} --all-name --with-gnome

# no *.la for modules nor static modules - shut up check files
%{__rm} $RPM_BUILD_ROOT%{gstlibdir}/lib*.{la,a}
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
%attr(755,root,root) %{_bindir}/gst-stats-1.0
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
%if "%{_libexecdir}" != "%{_libdir}"
%dir %{gstlibexecdir}
%endif
%attr(755,root,root) %{gstlibexecdir}/gst-plugin-scanner
%attr(755,root,root) %{gstlibexecdir}/gst-ptp-helper
%dir %{gstlibdir}
%attr(755,root,root) %{gstlibdir}/libgstcoreelements.so
%attr(755,root,root) %{gstlibdir}/libgstcoretracers.so
%{_mandir}/man1/gst-inspect-1.0.1*
%{_mandir}/man1/gst-launch-1.0.1*
%{_mandir}/man1/gst-stats-1.0.1*
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
%dir %{gstincludedir}
%{gstincludedir}/gst
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

%files -n bash-completion-gstreamer
%defattr(644,root,root,755)
%{bash_compdir}/gst-inspect-1.0
%{bash_compdir}/gst-launch-1.0
%attr(755,root,root) %{gstlibexecdir}/gst-completion-helper
%attr(755,root,root) %{_datadir}/bash-completion/helpers/gst
