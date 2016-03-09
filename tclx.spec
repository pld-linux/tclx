Summary:	Extended Tcl (TclX)
Summary(pl.UTF-8):	Rozszerzony Tcl (TclX)
Name:		tclx
%define	major	8.4
Version:	%{major}.1
Release:	1
License:	BSD-like
Group:		Development/Languages/Tcl
Source0:	http://downloads.sourceforge.net/tclx/%{name}%{version}.tar.bz2
# Source0-md5:	ac983708f23cf645c07058148f48440c
URL:		http://tclx.sourceforge.net/
BuildRequires:	tcl-devel >= %{major}
Requires:	tcl >= %{major}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Extended Tcl (TclX), is an extension to Tcl, the Tool Command Language
invented by Dr. John Ousterhout. Tcl is a powerful, yet simple
embeddable programming language. Extended Tcl is oriented towards
system programming tasks and large application development. TclX
provides additional interfaces to the operating system, and adds many
new programming constructs, text manipulation tools, and debugging
tools.

%description -l pl.UTF-8
TclX (Extended Tcl - rozszerzony Tcl) to rozszerzenie dla języka Tcl
(Tool Command Language - języka poleceń narzędziowych), wymyślonego
przez Dr. Johna Ousterhouta. Tcl to potężny, ale prosty osadzalny
język programowania. Extended Tcl jest zorientowany na programowanie
systemowe i tworzenie dużych aplikacji. TclX udostępnia wiele
dodatkowych interfejsów do systemu operacyjnego i dodaje wiele nowych
konstrukcji programistycznych, narzędzi do obróbki tekstu oraz
narzędzi diagnostycznych.

%package devel
Summary:	TclX header files
Summary(pl.UTF-8):	Pliki nagłówkowe TclX
Group:		Development/Languages/Tcl
Requires:	%{name} = %{version}-%{release}
Requires:	tcl-devel >= %{major}

%description devel
TclX header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe TclX.

%prep
%setup -q -n %{name}%{major}

%build
%configure \
	--enable-64bit \
	--enable-shared \
	--enable-threads
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# not covered by make install
install -d $RPM_BUILD_ROOT%{_mandir}/man3
cp -p doc/*.3 $RPM_BUILD_ROOT%{_mandir}/man3

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README license.terms
%dir %{_libdir}/tclx%{major}
%attr(755,root,root) %{_libdir}/tclx%{major}/libtclx%{major}.so
%{_libdir}/tclx%{major}/*.tcl
%{_mandir}/mann/TclX.n*

%files devel
%defattr(644,root,root,755)
%{_includedir}/tclExtend.h
%{_mandir}/man3/CmdWrite.3*
%{_mandir}/man3/Handles.3*
%{_mandir}/man3/Keylist.3*
%{_mandir}/man3/ObjCmdWrite.3*
%{_mandir}/man3/TclXInit.3*
