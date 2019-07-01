Summary: Dynomite, inspired by Dynamo white-paper, is a thin, distributed dynamo layer for different storage engines and protocols.
Name:    dynomite
Version: 0.7.1
Release: 1%{?dist}
License: ASL 2.0
Group:   Applications/Databases
URL:     https://github.com/Netflix/dynomite
Source0: https://github.com/Netflix/dynomite/archive/%{name}-%{version}.tar.gz
Source1: dynomite.service
Patch01: dynomite.configure.ac.patch

Requires(pre):    /usr/sbin/useradd
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%{?systemd_requires}
BuildRequires: systemd
BuildRequires: autoconf
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Dynomite, inspired by Dynamo whitepaper, is a thin, distributed dynamo layer for different
storage engines and protocols. Currently these include Redis and Memcached. Dynomite supports
multi-datacenter replication and is designed for high availability.
The ultimate goal with Dynomite is to be able to implement high availability and cross-datacenter
replication on storage engines that do not inherently provide that functionality.
The implementation is efficient, not complex (few moving parts), and highly performant.

%prep
%setup -q
%patch01 -p1
echo -n %{version} > VERSION
autoreconf -fvi


%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/dynomite.service
mkdir -p %{buildroot}%{_sysconfdir}/dynomite
mkdir -p %{buildroot}%{_var}/run/dynomite
mkdir -p %{buildroot}%{_var}/log/dynomite
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}/examples
cp -a LICENSE %{buildroot}%{_docdir}/%{name}-%{version}
cp -a README.md %{buildroot}%{_docdir}/%{name}-%{version}
cp -a conf/*.yml %{buildroot}%{_docdir}/%{name}-%{version}/examples

%clean
rm -rf %{buildroot}

%pre
if [ $1 -eq 1 ]; then
    /usr/sbin/useradd -c "Dynomite server" -s /sbin/nologin -r -d %{_var}/run/dynomite dynomite &>/dev/null || :
fi

%post
%systemd_post dynomite.service
chown dynomite:dynomite /var/log/dynomite

%preun
%systemd_preun dynomite.service

%postun
%systemd_postun dynomite.service

%files
%defattr(-,root,root,-)
%{_sbindir}/dynomite
%{_sbindir}/dynomite-test
%{_bindir}/dynomite-hash-tool
%{_unitdir}/dynomite.service
%dir %{_var}/run/dynomite/
%dir %{_var}/log/dynomite/
%dir %{_sysconfdir}/dynomite
%{_mandir}/man8/*
%{_docdir}/%{name}-%{version}

%changelog
* Thu Jun 20 2019 Jüri Palis <karvik.kimalane@gmail.com> - 0.7.1-1
- Update to 0.7.1, which adds support for all X* (streams) commands
* Mon May 27 2019 Jüri Palis <karvik.kimalane@gmail.com> - 0.7.0-1
- Initial RPM version
