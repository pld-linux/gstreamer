Summary:	GStreamer Streaming-media framework runtime
Name:		gstreamer
Version:	0.1.1
Release:	1
License:	LGPL
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Source0:	%{name}-%{version}.tar.gz
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
%configure2_13

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
