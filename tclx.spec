# TODO: mv *.tcl ulibdir ?
Summary:	Extended Tcl (TclX)
Summary(pl.UTF-8):	Rozszerzony Tcl (TclX)
Name:		tclx
%define	major	8.4
Version:	%{major}
Release:	0.1
License:	BSD
Group:		Development/Languages/Tcl
Source0:	http://dl.sourceforge.net/tclx/%{name}%{version}.tar.bz2
# Source0-md5:	395c2fbe35e1723570b005161b9fc8f8
URL:		http://tclx.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	tcl-devel >= %{major}.0
BuildRequires:	tk-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_ulibdir /usr/lib

%if "%{_libdir}" != "%{_ulibdir}"
%define have_ulibdir 1
%endif

%description
TclX extension to Tcl.

%description -l pl.UTF-8
TclX - rozszerzenie do Tcl.

%package devel
Summary:	Tool Command Language header files
Summary(pl.UTF-8):	Pliki nagłówkowe dla Tcl (Tool Command Language)
Group:		Development/Languages/Tcl
Requires:	%{name} = %{version}-%{release}

%description devel
Tool Command Language embeddable scripting language header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla Tcl (Tool Command Language).

%prep
%setup -q -n %{name}%{version}

%build
%configure \
	--enable-threads \
	--enable-shared \
	--enable-64bit
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%dir %{_libdir}/tclx%{major}
%{_libdir}/tclx%{major}/*.tcl
%attr(755,root,root) %{_libdir}/tclx%{major}/*.so
%{_mandir}/mann/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
