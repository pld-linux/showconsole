Summary:	Small daemon for logging console output during boot
Summary(pl.UTF-8):	Mały demon do logowania wyjścia konsoli w czasie startu systemu
Name:		showconsole
Version:	1.10
Release:	2
License:	GPL v2
Group:		Base
Source0:	ftp://ftp.suse.com/pub/projects/init/%{name}-%{version}.tar.bz2
# Source0-md5:	f0d9d76e1de0d6b4cff57f6b5f9ff523
Patch0:		%{name}-quiet.patch
Patch1:		%{name}-lib64.patch
Patch2:		%{name}-suse.patch
URL:		ftp://ftp.suse.com/pub/projects/init/
BuildRequires:	linux-libc-headers >= 7:2.6.12.0-15
BuildRequires:	sed >= 4.0
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
%patch1 -p1
%patch2 -p0

# match path with plymouth
grep -rl /var/log/boot.msg . | xargs sed -i -e 's,/var/log/boot.msg,/var/log/boot.log,'

%build
%{__make} \
	COPTS="%{rpmcflags}" \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/dev,/var/log}
%{__make} install \
	lib=%{_lib} \
	DESTDIR=$RPM_BUILD_ROOT

touch $RPM_BUILD_ROOT/var/log/boot.msg
touch $RPM_BUILD_ROOT/dev/blog

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -p /dev/blog ]; then
	mknod -m 640 /dev/blog p
fi

%files
%defattr(644,root,root,755)
%doc showconsole-*.lsm README
%attr(755,root,root) %{_sbindir}/blogd
%attr(755,root,root) %{_sbindir}/blogger
%attr(755,root,root) %{_sbindir}/isserial
%attr(755,root,root) %{_sbindir}/setconsole
%attr(755,root,root) %{_sbindir}/showconsole
%{_mandir}/man8/blogd.8*
%{_mandir}/man8/blogger.8*
%{_mandir}/man8/isserial.8*
%{_mandir}/man8/setconsole.8*
%{_mandir}/man8/showconsole.8*
%ghost /var/log/boot.msg
%attr(640,root,root) %ghost /dev/blog

%files devel
%defattr(644,root,root,755)
%{_includedir}/libblogger.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libblogger.a
