%include	/usr/lib/rpm/macros.mono
Summary:	Mono.Zeroconf provides an easy to use API that covers the most common operations for mDNS
Name:		dotnet-mono-zeroconf
Version:	0.7.3
Release:	1
# no real license information, just included COPYING
License:	LGPL v2
Group:		Libraries
Source0:	http://banshee-project.org/files/mono-zeroconf/mono-zeroconf-%{version}.tar.bz2
# Source0-md5:	d63ccff9ac8554f24a066a51e244df32
URL:		http://mono-project.com/Mono.Zeroconf
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	avahi-compat-libdns_sd-devel
BuildRequires:	dotnet-avahi-devel
BuildRequires:	libtool
BuildRequires:	mono-csharp >= 1.1.16.1
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(monoautodeps)
ExcludeArch:	i386
# can't be noarch because of pkgconfigdir (use /usr/share/pkgconfig?)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mono.Zeroconf provides an easy to use API that covers the most common operations for mDNS.

%package provider-avahi
Summary:	Avahi provider for Mono.Zeroconf
Group:		Libraries
Provides:	dotnet-mono-zeroconf-provider
Requires:	%{name} = %{version}-%{release}

%description provider-avahi
This package provides an Avahi Zeroconf provider for Mono.Zeroconf.

%package provider-mDNSResponder
Summary:	Bonjour provider for Mono.Zeroconf
Group:		Libraries
Provides:	dotnet-mono-zeroconf-provider
Requires:	%{name} = %{version}-%{release}

%description provider-mDNSResponder
This package provides an mDNSResponder Zeroconf provider for Mono.Zeroconf.

%prep
%setup -qn mono-zeroconf-%{version}

%build
%{__libtoolize}
%{__aclocal} -I .
%{__autoconf}
%{__automake}
%configure \
	--enable-avahi

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/mzclient
%dir %{_prefix}/lib/mono-zeroconf
%{_prefix}/lib/mono-zeroconf/MZClient.exe*
%dir %{_prefix}/lib/mono/mono-zeroconf
%{_prefix}/lib/mono/mono-zeroconf/Mono.Zeroconf.dll*
%{_prefix}/lib/mono/gac/Mono.Zeroconf
%{_pkgconfigdir}/mono-zeroconf.pc

%files provider-avahi
%defattr(644,root,root,755)
%{_prefix}/lib/mono-zeroconf/Mono.Zeroconf.Providers.Avahi.dll*

%files provider-mDNSResponder
%defattr(644,root,root,755)
%{_prefix}/lib/mono-zeroconf/Mono.Zeroconf.Providers.Bonjour.dll*
