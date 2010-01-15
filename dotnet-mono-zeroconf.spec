#
# Conditional build:
%bcond_with	mdns		# build with mDNSResponder support
#
%include	/usr/lib/rpm/macros.mono
#
Summary:	Mono.Zeroconf - easy to use API that covers the most common operations for mDNS
Summary(pl.UTF-8):	Mono.Zeroconf - łatwe w użyciu API pokrywające większość operacji mDNS
Name:		dotnet-mono-zeroconf
Version:	0.9.0
Release:	3
License:	MIT
Group:		Libraries
Source0:	http://banshee-project.org/files/mono-zeroconf/mono-zeroconf-%{version}.tar.bz2
# Source0-md5:	cb25d50898442a7766c324dcb52ef9bf
Patch0:		%{name}-pkgconfig.patch
URL:		http://mono-project.com/Mono.Zeroconf
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.9
BuildRequires:	avahi-compat-libdns_sd-devel
BuildRequires:	dotnet-avahi-devel >= 0.6.0
BuildRequires:	mono-csharp >= 1.1.16.1
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(monoautodeps)
Requires:	%{name}-provider = %{version}-%{release}
ExcludeArch:	i386
# can't be noarch because of pkgconfigdir (use /usr/share/pkgconfig?)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mono.Zeroconf provides an easy to use API that covers the most common
operations for mDNS.

%description -l pl.UTF-8
Mono.Zeroconf udostępnia łatwe w użyciu API pokrywające większość
popularnych operacji mDNS.

%package devel
Summary:	Development files for Mono.Zeroconf library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki Mono.Zeroconf
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for Mono.Zeroconf library.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki Mono.Zeroconf.

%package provider-avahi
Summary:	Avahi provider for Mono.Zeroconf
Summary(pl.UTF-8):	Łącznik Avahi dla biblioteki Mono.Zeroconf
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-provider = %{version}-%{release}

%description provider-avahi
This package provides an Avahi Zeroconf provider for Mono.Zeroconf.

%description provider-avahi -l pl.UTF-8
Ten pakiet udostępnia łącznik z Avahi dla biblioteki Mono.Zeroconf.

%package provider-mDNSResponder
Summary:	Bonjour provider for Mono.Zeroconf
Summary(pl.UTF-8):	Łącznik Bonjour dla biblioteki Mono.Zeroconf
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
%ifarch %{x8664} ia64 ppc64 s390x sparc64
Requires:	libnss_mdns-0.2.so()(64bit)
%else
Requires:	libnss_mdns-0.2.so
%endif
Provides:	%{name}-provider = %{version}-%{release}

%description provider-mDNSResponder
This package provides an mDNSResponder Zeroconf provider for
Mono.Zeroconf.

%description provider-mDNSResponder -l pl.UTF-8
Ten pakiet udostępnia łącznik z usługą Zeroconf mDNSRespondera dla
biblioteki Mono.Zeroconf.

%prep
%setup -q -n mono-zeroconf-%{version}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I .
%{__autoconf}
%{__automake}
%configure \
	--enable-avahi \
	--libdir=/%{_prefix}/lib \
	--libexecdir=%{_libdir} \
	--%{?with_mdns:en}%{!?with_mdns:dis}able-mdnsresponder

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT{%{_prefix}/lib/pkgconfig,%{_datadir}}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/mzclient
# .mdb to -debug?
%{_prefix}/lib/mono/gac/Mono.Zeroconf
%{_prefix}/lib/mono/gac/policy.1.0.Mono.Zeroconf
%{_prefix}/lib/mono/gac/policy.2.0.Mono.Zeroconf
%{_prefix}/lib/mono/gac/policy.3.0.Mono.Zeroconf
%{_prefix}/lib/mono/gac/policy.4.0.Mono.Zeroconf
%dir %{_prefix}/lib/mono-zeroconf
%{_prefix}/lib/mono-zeroconf/MZClient.exe
# -debug?
%{_prefix}/lib/mono-zeroconf/MZClient.exe.mdb

%files devel
%defattr(644,root,root,755)
%dir %{_prefix}/lib/mono/mono-zeroconf
%{_prefix}/lib/mono/mono-zeroconf/Mono.Zeroconf.dll
%{_datadir}/pkgconfig/mono-zeroconf.pc
%{_libdir}/monodoc/sources/mono-zeroconf-docs.*

%files provider-avahi
%defattr(644,root,root,755)
%{_prefix}/lib/mono-zeroconf/Mono.Zeroconf.Providers.AvahiDBus.dll
# -debug?
%{_prefix}/lib/mono-zeroconf/Mono.Zeroconf.Providers.AvahiDBus.dll.mdb

%if %{with mdns}
%files provider-mDNSResponder
%defattr(644,root,root,755)
%{_prefix}/lib/mono-zeroconf/Mono.Zeroconf.Providers.Bonjour.dll
%{_prefix}/lib/mono-zeroconf/Mono.Zeroconf.Providers.Bonjour.dll.config
# -debug?
%{_prefix}/lib/mono-zeroconf/Mono.Zeroconf.Providers.Bonjour.dll.mdb
%endif
