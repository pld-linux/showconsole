Summary:	Small daemon for logging console output during boot
Summary(pl.UTF-8):	Mały demon do logowania wyjścia konsoli w czasie startu systemu
Name:		showconsole
Version:	1.08
Release:	1
License:	GPL v2
Group:		Base
Source0:	ftp://ftp.suse.com/pub/projects/init/%{name}-%{version}.tar.gz
# Source0-md5:	351daafbf394a1602e92c7c9afe13a6a
Patch0:		%{name}-no-TIOCGDEV.patch
Patch1:		%{name}-quiet.patch
Patch2:		%{name}-lib64.patch
URL:		ftp://ftp.suse.com/pub/projects/init/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
This small package provides a daemon for logging during boot time of
System V boot.

%description -l pl.UTF-8
Ten mały pakiet udosępnia demona do logowania w czasie startu systemu
w stylu SysV.

%package devel
Summary:	Header files for libblogger library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libblogger
Group:		Development/Libraries

%description devel
This is the package containing the header file for libblogger library.

%description devel -l pl.UTF-8
Ten pakiet zawiera plik nagłówkowy biblioteki libblogger.

%package static
Summary:	Static libblogger library
Summary(pl.UTF-8):	Statyczna biblioteka libblogger
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libblogger library.

%description static -l pl.UTF-8
Statyczna biblioteka libblogger.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p1

%build
%{__make} \
	COPTS="%{rpmcflags}" \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	lib=%{_lib} \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc showconsole-*.lsm README
%attr(755,root,root) %{_sbindir}/blogd
%attr(755,root,root) %{_sbindir}/blogger
%attr(755,root,root) %{_sbindir}/isserial
%attr(755,root,root) %{_sbindir}/showconsole
%{_mandir}/man8/blogd.8*
%{_mandir}/man8/blogger.8*
%{_mandir}/man8/isserial.8*
%{_mandir}/man8/setconsole.8*
%{_mandir}/man8/showconsole.8*

%files devel
%defattr(644,root,root,755)
%{_includedir}/libblogger.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libblogger.a
