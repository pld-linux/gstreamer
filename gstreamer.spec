Summary:	GStreamer Streaming-media framework runtime
Summary(pl):	GStreamer - biblioteki ¶rodowiska do obróbki strumieni
Name:		gstreamer
Version:	0.4.1
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://prdownloads.sourceforge.net/gstreamer/%{name}-%{version}.tar.bz2
URL:		http://gstreamer.net/
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	libxml2-devel >= 2.4.17
BuildRequires:	nasm
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
rzeczywistym, do odtwarzania filmów i czegokolwiek innego zwi±zego z
mediami. Architektura bazuj±ca na wtyczkach pozwala na ³atwe dodawanie
nowych typów danych lub mo¿liwo¶ci obróbki.

%package devel
Summary:	Include files for GStreamer streaming-media framework
Summary(pl):	Pliki nag³ówkowe do ¶rodowiska obróbki strumieni GStreamer
Group:		Development/Libraries
Requires:	%{name} = %{version}

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
Requires:	%{name}-devel = %{version}

%description static
Static versions of GStreamer libraries.

%description static -l pl
Statyczne wersje bibliotek GStreamer.

%prep
%setup -q

%build
%configure \
	--enable-glib2 \
	--enable-libmmx \
	--enable-atomic

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%{_bindir}/gst-register --gst-mask=0

%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*
%attr(755,root,root) %{_libdir}/gst/*.so*
%attr(755,root,root) %{_libdir}/gst/*.la
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/%{name}-%{version}
%{_pkgconfigdir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%{_libdir}/gst/lib*.a
