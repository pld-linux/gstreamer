Summary:	GStreamer Streaming-media framework runtime
Summary(pl):	GStreamer - biblioteki ¶rodowiska do obróbki strumieni
Name:		gstreamer
Version:	0.7.1
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/0.7/%{name}-%{version}.tar.bz2
# Source0-md5:	cae564f506614a9bb9e351d23070d6ab
#Patch0:		%{name}-libtool.patch
Patch0:		%{name}-without_ps_pdf.patch
Patch1:		%{name}-doc-destdir.patch
Patch2:		%{name}-doc-build.patch
URL:		http://gstreamer.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	glib2-devel >= 2.0.1
BuildRequires:	gtk-doc >= 0.7
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.4.17
BuildRequires:	nasm
BuildRequires:	pkgconfig
BuildRequires:	popt-devel >= 1.6.1
BuildRequires:	transfig
BuildRequires:	xmlto
Requires(post):	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_gstlibdir	%{_libdir}/gstreamer-0.7
%define		_gstincludedir	%{_includedir}/gstreamer-0.7
%define		_gstcachedir	%{_var}/cache/gstreamer

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
Requires:	glib2-devel >= 2.0.1
Requires:	libxml2-devel >= 2.4.17
Requires:	popt-devel >= 1.6.1

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
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
intltoolize --copy --force
#%%{__gettextize}
%{__libtoolize}
%{__aclocal} -I common/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--program-suffix="" \
%ifarch i586 i686 athlon
	--enable-fast-stack-trash \
%else
	--disable-fast-stack-trash \
%endif
	--enable-glib2 \
	--enable-libmmx \
	--enable-atomic \
	--disable-examples \
	--disable-tests \
	--disable-debug \
	--disable-debug-color \
	--enable-docs-build \
	--with-html-dir=%{_gtkdocdir} \
	--with-cachedir=%{_gstcachedir}
	
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT


install -d $RPM_BUILD_ROOT%{_gstcachedir}
touch $RPM_BUILD_ROOT%{_gstcachedir}/registry.xml

%find_lang %{name} --all-name --with-gnome

# no static modules and *.la for them - shut up check files
rm -f $RPM_BUILD_ROOT%{_gstlibdir}/lib*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
# how to do it ????
%{_bindir}/gst-register --gst-registry=%{_gstcachedir}/registry.xml
#%%{_bindir}/gst-register --gst-mask=0

%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README RELEASE NEWS TODO ChangeLog
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%dir %{_gstlibdir}
%attr(755,root,root) %{_gstlibdir}/*.so
%dir %{_gstcachedir}
%ghost %{_gstcachedir}/registry.xml
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_gstincludedir}
%{_gtkdocdir}/*
%{_pkgconfigdir}/*
%{_aclocaldir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
