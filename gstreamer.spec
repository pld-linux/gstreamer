Summary:	GStreamer Streaming-media framework runtime
Name:		gstreamer
Version:	0.2.2
Release:	0.20011125.1
License:	LGPL
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Source0:	http://download.sourceforge.net/gstreamer/%{name}.tar.bz2
#Source0:	http://download.sourceforge.net/gstreamer/%{name}-%{version}.tar.bz2
Patch0:		%{name}-size_t.patch
URL:		http://gstreamer.net
BuildRequires:	nasm
BuildRequires:	pkgconfig
BuildRequires:	GConf-devel
BuildRequires:	Hermes-devel
BuildRequires:	SDL-devel
BuildRequires:	aalib-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	arts-devel
BuildRequires:	audiofile-devel
BuildRequires:	avifile-devel
BuildRequires:	cdparanoia-III-devel
BuildRequires:	esound-devel
BuildRequires:	gdk-pixbuf-devel
BuildRequires:	gnome-libs-devel
BuildRequires:	gnome-vfs-devel
BuildRequires:	gtk+-devel
BuildRequires:	lame-libs-devel
BuildRequires:	libdv-devel
BuildRequires:	libdvdread-devel
BuildRequires:	libghttp-devel
BuildRequires:	libglade-devel
BuildRequires:	libgsm-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libmikmod-devel
BuildRequires:	libraw1394-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libxml-devel
BuildRequires:	mad-devel
BuildRequires:	mpeg2dec-devel
BuildRequires:	quicktime4linux-devel
BuildRequires:	xmms-devel

# libshout 1.0.5 is out of date...
# http://cvs.icecast.org/cvsweb.cgi/
# module shout
#BuildRequires:	libshout-devel

BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GStreamer is a streaming-media framework, based on graphs of filters
which operate on media data. Applications using this library can do
anything from real-time sound processing to playing videos, and just
about anything else media-related. Its plugin-based architecture means
that new data types or processing capabilities can be added simply by
installing new plugins.

%package devel
Summary:	Libraries and include files for GStreamer streaming-media framework
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
GStreamer is a streaming-media framework, based on graphs of filters
which operate on media data. Applications using this library can do
anything from real-time sound processing to playing videos, and just
about anything else media-related. Its plugin-based architecture means
that new data types or processing capabilities can be added simply by
installing new plugins.

This package contains the libraries and includes files necessary to
develop applications and plugins for GStreamer.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
rm -f missing
./makeconfigure < configure.base > configure.in configure.in
libtoolize --force --copy
aclocal
automake --add-missing
autoconf
%configure \
	--enable-libmmx \
	--enable-libghttp \
	--enable-alsa \
	--enable-libxmms \
	--enable-gdk_pixbuf \
	--enable-libaudiofile \
	--enable-libesd \
	--enable-arts \
	--enable-atomic \
	--enable-autoplug

%{__make}

%install  
rm -rf $RPM_BUILD_ROOT
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%{__make} DESTDIR=$RPM_BUILD_ROOT install

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%{prefix}/bin/gstreamer-register

%postun
/sbin/ldconfig
  
%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_libdir}/lib*.so.*
%{_libdir}/gst/*
%{_datadir}/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%{_libdir}/lib*.a
%{_libdir}/lib*.so
