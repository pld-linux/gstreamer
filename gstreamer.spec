Summary:	GStreamer Streaming-media framework runtime
Name:		gstreamer
Version:	0.2.1
Release:	1
License:	LGPL
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Source0:	http://download.sourceforge.net/gstreamer/%{name}-%{version}.tar.bz2
URL:		http://gstreamer.net
BuildRequires:	gtk+-devel
BuildRequires:	libxml-devel
BuildRequires:	arts-devel
BuildRequires:	xmms-devel
BuildRequires:	gdk-pixbuf-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	audiofile-devel
BuildRequires:	esound-devel
BuildRequires:	libglade-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libghttp-devel
BuildRequires:	Hermes-devel
BuildRequires:	avifile-devel
BuildRequires:	libraw1394-devel
BuildRequires:	gnome-libs-devel
BuildRequires:	gnome-vfs-devel
BuildRequires:	mpeg2dec-devel
BuildRequires:	libshout-devel
BuildRequires:	libgsm-devel
BuildRequires:	cdparanoia-III-devel
BuildRequires:	lame-libs-devel
BuildRequires:	libdv-devel
BuildRequires:	aalib-devel
#BuildRequires:	quicktime4linux-devel
BuildRequires:	SDL-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6

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
Requires:	%{name}

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
%setup -q

%build
rm missing
#LDFLAGS="-L/usr/X11R6/lib"
#autoconf
%configure \
	--prefix=%{_prefix} \
	--enable-libmmx \
	--enable-libghttp \
	--enable-gdk_pixbuf \
	--enable-libaudiofile \
	--enable-alsa \
	--enable-libxmms \
	--enable-libesd \
	--enable-arts \
	--disable-atomic \
	--enable-autoplug

%{__make}

%install  
rm -rf $RPM_BUILD_ROOT
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%{__make} prefix=$RPM_BUILD_ROOT%{_prefix} install

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
