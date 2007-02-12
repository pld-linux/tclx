Summary:	Extended Tcl (TclX)
Summary(pl.UTF-8):   Rozszerzony Tcl (TclX)
Name:		tclx
%define	major	8.3
Version:	%{major}.5
Release:	1
License:	BSD
Group:		Development/Languages/Tcl
Source0:	http://dl.sourceforge.net/tclx/%{name}%{version}-src.tar.gz
# Source0-md5:	2cdd06d29f6dfbf31bf4ce192cf46918
Patch0:		%{name}-skiptest.patch
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
Summary(pl.UTF-8):   Pliki nagłówkowe dla Tcl (Tool Command Language)
Group:		Development/Languages/Tcl
Requires:	%{name} = %{version}-%{release}

%description devel
Tool Command Language embeddable scripting language header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla Tcl (Tool Command Language).

%prep
%setup -q -n %{name}%{version}
%patch0 -p1

%build
cd unix
sed -i -e "s/^CFLAGS_OPTIMIZE.*/CFLAGS_OPTIMIZE=%{rpmcflags} -D__NO_STRING_INLINES -D__NO_MATH_INLINES -D_REENTRANT/" \
	Makefile.in
%configure2_13 \
	--with-tclconfig=%{_ulibdir} \
        --with-tkconfig=%{_ulibdir} \
        --with-tclinclude=%{_includedir} \
        --with-tkinclude=%{_includedir} \
	--enable-shared \
	--enable-threads \
	--enable-64bit \
	--enable-gcc
%{__make} \
	TCL_PACKAGE_PATH="%{_libdir} %{_libdir}/tcl%{major} %{_ulibdir} %{_ulibdir}/tcl%{major}"

sed -i -e "s#%{_builddir}/%{name}%{version}/unix#%{_libdir}#g" t*Config.sh

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_prefix},%{_mandir}/man1}

%{__make} -C unix install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	TCL_PACKAGE_PATH="%{_libdir} %{_libdir}/tcl%{major} %{_ulibdir} %{_ulibdir}/tcl%{major}" \
	MAN_INSTALL_DIR=$RPM_BUILD_ROOT%{_mandir}

# for linking with -ltclx and -ltkx
ln -sf libtclx%{major}.so $RPM_BUILD_ROOT%{_libdir}/libtclx.so
ln -sf libtkx%{major}.so $RPM_BUILD_ROOT%{_libdir}/libtkx.so
ln -sf libtclx%{major}.a $RPM_BUILD_ROOT%{_libdir}/libtclx.a
ln -sf libtkx%{major}.a $RPM_BUILD_ROOT%{_libdir}/libtkx.a

# rename memory.n since tcl-devel also provides it
mv $RPM_BUILD_ROOT%{_mandir}/mann/{m,M}emory.n

%{?have_ulibdir:mv $RPM_BUILD_ROOT%{_libdir}/t*Config.sh $RPM_BUILD_ROOT%{_ulibdir}}

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
