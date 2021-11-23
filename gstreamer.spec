# TODO: suid/capabilities for ptp-helper?
%define		gstmver		1.0

Summary:	GStreamer Streaming-media framework runtime
Summary(pl.UTF-8):	GStreamer - biblioteki środowiska do obróbki strumieni
Name:		gstreamer
Version:	1.19.3
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://gstreamer.freedesktop.org/src/gstreamer/%{name}-%{version}.tar.xz
# Source0-md5:	5af65dab2d400fbc5a9850b16bb5db05
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
BuildRequires:	hotdoc
BuildRequires:	libcap-devel
BuildRequires:	libtool >= 2:2.2.6
%ifarch %{ix86} %{x8664} x32 %{arm} hppa ia64 mips ppc ppc64 sh
BuildRequires:	libunwind-devel
%endif
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	python >= 2.1
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.726
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.40.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		gstlibdir	%{_libdir}/gstreamer-%{gstmver}
%define		gstlibexecdir	%{_libexecdir}/gstreamer-%{gstmver}
%define		gstincludedir	%{_includedir}/gstreamer-%{gstmver}

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
Conflicts:	gstreamer-plugins-bad-devel < 1.14

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

%package gdb
Summary:	GStreamer pretty printers for GDB
Summary(pl.UTF-8):	Funkcje wypisujące dane GStreamer dla GDB
Group:		Development/Debuggers

%description gdb
This package contains Python scripts for GDB pretty printing of the
GStreamer types.

%description gdb -l pl.UTF-8
Ten pakiet zawiera skrypty Pythona dla GDB służące do ładnego
wypisywania typów GStreamer.

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

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python3(\s|$),#!%{__python3}\1,' \
      docs/gst-plugins-doc-cache-generator.py

%build
%meson build \
	-D doc=enabled \
	-D tests=disabled \
	-D examples=disabled

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%find_lang %{name} --all-name --with-gnome

# no static modules - shut up check files
%{__rm} $RPM_BUILD_ROOT%{gstlibdir}/lib*.a

%py_comp $RPM_BUILD_ROOT%{_datadir}/gstreamer-1.0/gdb/
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/gstreamer-1.0/gdb/
%py_postclean %{_datadir}/gstreamer-1.0/gdb/

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
%attr(755,root,root) %{_libdir}/libgstbase-%{gstmver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstbase-%{gstmver}.so.0
%attr(755,root,root) %{_libdir}/libgstcheck-%{gstmver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstcheck-%{gstmver}.so.0
%attr(755,root,root) %{_libdir}/libgstcontroller-%{gstmver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstcontroller-%{gstmver}.so.0
%attr(755,root,root) %{_libdir}/libgstnet-%{gstmver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstnet-%{gstmver}.so.0
%attr(755,root,root) %{_libdir}/libgstreamer-%{gstmver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstreamer-%{gstmver}.so.0
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
%{_libdir}/girepository-1.0/Gst-%{gstmver}.typelib
%{_libdir}/girepository-1.0/GstBase-%{gstmver}.typelib
%{_libdir}/girepository-1.0/GstCheck-%{gstmver}.typelib
%{_libdir}/girepository-1.0/GstController-%{gstmver}.typelib
%{_libdir}/girepository-1.0/GstNet-%{gstmver}.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgstbase-%{gstmver}.so
%attr(755,root,root) %{_libdir}/libgstcheck-%{gstmver}.so
%attr(755,root,root) %{_libdir}/libgstcontroller-%{gstmver}.so
%attr(755,root,root) %{_libdir}/libgstnet-%{gstmver}.so
%attr(755,root,root) %{_libdir}/libgstreamer-%{gstmver}.so
%dir %{gstincludedir}
%{gstincludedir}/gst
%{_pkgconfigdir}/gstreamer-%{gstmver}.pc
%{_pkgconfigdir}/gstreamer-base-%{gstmver}.pc
%{_pkgconfigdir}/gstreamer-check-%{gstmver}.pc
%{_pkgconfigdir}/gstreamer-controller-%{gstmver}.pc
%{_pkgconfigdir}/gstreamer-net-%{gstmver}.pc
%{_aclocaldir}/gst-element-check-%{gstmver}.m4
%{_datadir}/gir-1.0/Gst-%{gstmver}.gir
%{_datadir}/gir-1.0/GstBase-%{gstmver}.gir
%{_datadir}/gir-1.0/GstCheck-%{gstmver}.gir
%{_datadir}/gir-1.0/GstController-%{gstmver}.gir
%{_datadir}/gir-1.0/GstNet-%{gstmver}.gir
%{_libdir}/gstreamer-1.0/pkgconfig/gstcoreelements.pc
%{_libdir}/gstreamer-1.0/pkgconfig/gstcoretracers.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libgstbase-%{gstmver}.a
%{_libdir}/libgstcheck-%{gstmver}.a
%{_libdir}/libgstcontroller-%{gstmver}.a
%{_libdir}/libgstnet-%{gstmver}.a
%{_libdir}/libgstreamer-%{gstmver}.a

%if 0
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gstreamer-%{gstmver}
%{_gtkdocdir}/gstreamer-libs-%{gstmver}
%{_gtkdocdir}/gstreamer-plugins-%{gstmver}
%endif

%files gdb
%defattr(644,root,root,755)
%{_datadir}/gdb/auto-load%{_libdir}/libgstreamer-%{gstmver}.so.*.*.*-gdb.py
%dir %{_datadir}/gstreamer-1.0
%{_datadir}/gstreamer-1.0/gdb

%files -n bash-completion-gstreamer
%defattr(644,root,root,755)
%{bash_compdir}/gst-inspect-1.0
%{bash_compdir}/gst-launch-1.0
%attr(755,root,root) %{gstlibexecdir}/gst-completion-helper
%attr(755,root,root) %{_datadir}/bash-completion/helpers/gst
