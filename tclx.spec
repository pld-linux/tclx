Summary:	Extended Tcl (TclX)
Name:		tclx
%define	major	8.3
Version:	%{major}.5
Release:	1
License:	BSD
Group:		Development/Languages/Tcl
Source0:	http://dl.sourceforge.net/tclx/%{name}%{version}-src.tar.gz
# Source0-md5:	2cdd06d29f6dfbf31bf4ce192cf46918
URL:		http://tclx.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	tcl-devel >= %{major}.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_ulibdir /usr/lib

%if "%{_libdir}" != "%{_ulibdir}"
%define have_ulibdir 1
%endif

%description
TclX extension to Tcl.

%package devel
Summary:	Tool Command Language header files and development documentation
Summary(pl):	Pliki nag³ówkowe oraz dokumentacja dla Tcl (Tool Command Language)
Group:		Development/Languages/Tcl
Requires:	%{name} = %{version}-%{release}

%description devel
Tool Command Language embeddable scripting language header files and
develpment documentation.

%description devel -l pl
Pliki nag³ówkowe oraz dokumentacja dla Tcl (Tool Command Language).

%prep
%setup -q -n %{name}%{version}

%build
cd unix
sed -e "s/^CFLAGS_OPTIMIZE.*/CFLAGS_OPTIMIZE=%{rpmcflags} -D__NO_STRING_INLINES -D__NO_MATH_INLINES -D_REENTRANT/" \
	Makefile.in > Makefile.in.new
mv -f Makefile.in.new Makefile.in
%configure2_13 \
	--enable-shared \
	--enable-threads \
	--enable-64bit \
	--enable-gcc
%{__make} \
	TCL_PACKAGE_PATH="%{_libdir} %{_libdir}/tcl%{major} %{_ulibdir} %{_ulibdir}/tcl%{major}"

sed -e "s#%{_builddir}/%{name}%{version}/unix#%{_libdir}#; \
	s#%{_builddir}/%{name}%{version}#%{_includedir}#" tclConfig.sh > tclConfig.sh.new
mv -f tclConfig.sh.new tclConfig.sh

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_prefix},%{_mandir}/man1}

%{__make} -C unix install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	TCL_PACKAGE_PATH="%{_libdir} %{_libdir}/tcl%{major} %{_ulibdir} %{_ulibdir}/tcl%{major}" \
	MAN_INSTALL_DIR=$RPM_BUILD_ROOT%{_mandir}

ln -sf libtcl%{major}.so.0.0 $RPM_BUILD_ROOT%{_libdir}/libtcl.so
ln -sf libtcl%{major}.so.0.0 $RPM_BUILD_ROOT%{_libdir}/libtcl%{major}.so
mv -f $RPM_BUILD_ROOT%{_bindir}/tclsh%{major} $RPM_BUILD_ROOT%{_bindir}/tclsh

%{?have_ulibdir:mv $RPM_BUILD_ROOT%{_libdir}/tclConfig.sh $RPM_BUILD_ROOT%{_ulibdir}/tclConfig.sh}

bzip2 -dc %{SOURCE1} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

install -d $RPM_BUILD_ROOT%{_libdir}/tcl%{major}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_libdir}/tcl%{major}
%{?have_ulibdir:%{_ulibdir}/tcl%{major}}
%{_mandir}/man1/*
%lang(pl) %{_mandir}/pl/man1/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_ulibdir}/tclConfig.sh
%{_libdir}/libtclstub%{major}.a
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*
%{_mandir}/man[3n]/*
%lang(pl) %{_mandir}/pl/mann/*
