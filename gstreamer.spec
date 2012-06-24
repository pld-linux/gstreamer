%define name    gstreamer
%define ver     0.1.1
%define rel     1
%define prefix  /usr

Summary: GStreamer Streaming-media framework runtime
Name: %name
Version: %ver
Release: %rel
Copyright: LGPL
Group: Libraries
Source: %{name}-%{ver}.tar.gz
BuildRoot: /var/tmp/%{name}-%{ver}-root
Docdir: %{prefix}/doc
Prefix: %prefix

%description
GStreamer is a streaming-media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new 
plugins.

%package devel
Summary: Libraries and include files for GStreamer streaming-media framework
Group: Development/Libraries
Requires: %{name}

%description devel
GStreamer is a streaming-media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new   
plugins.

This package contains the libraries and includes files necessary to develop
applications and plugins for GStreamer.

%changelog
* Tue Jan 09 2001 Erik Walthinsen <omega@cse.ogi.edu>
- updated to build -devel package as well

* Sun Jan 30 2000 Erik Walthinsen <omega@cse.ogi.edu>
- first draft of spec file

%prep
%setup

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%prefix

if [ "$SMP" != "" ]; then
  (make "MAKE=make -k -j $SMP"; exit 0)
  make
else
  make
fi

%install  
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

make prefix=$RPM_BUILD_ROOT%{prefix} install

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%{prefix}/bin/gstreamer-register

%postun
/sbin/ldconfig
  
%files
%defattr(-, root, root)
%{prefix}/bin/*
%{prefix}/lib/lib*.so.*
%{prefix}/lib/gst/*
%{prefix}/share/*

%files devel
%{prefix}/include/*
%{prefix}/lib/lib*.a
%{prefix}/lib/lib*.so
