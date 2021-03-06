Name:           puppet-manifests
Version:        1.0.0
Release:        %{tis_patch_ver}%{?_tis_dist}
Summary:        Puppet Configuration and Manifests
License:        Apache-2.0
Packager:       Wind River <info@windriver.com>
URL:            unknown

Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

# List all the required puppet modules

# WRS puppet modules
Requires: puppet-dcorch
Requires: puppet-dcmanager
Requires: puppet-mtce
Requires: puppet-nfv
Requires: puppet-nova_api_proxy
Requires: puppet-patching
Requires: puppet-sysinv
Requires: puppet-sshd
Requires: puppet-smapi
Requires: puppet-fm

# Openstack puppet modules
Requires: puppet-aodh
Requires: puppet-barbican
Requires: puppet-ceilometer
Requires: puppet-ceph
Requires: puppet-cinder
Requires: puppet-glance
Requires: puppet-heat
Requires: puppet-horizon
Requires: puppet-keystone
Requires: puppet-neutron
Requires: puppet-nova
Requires: puppet-openstacklib
Requires: puppet-swift
Requires: puppet-tempest
Requires: puppet-vswitch
Requires: puppet-murano
Requires: puppet-magnum
Requires: puppet-ironic
Requires: puppet-panko
Requires: puppet-memcached
Requires: puppet-gnocchi

# Puppetlabs puppet modules
Requires: puppet-concat
Requires: puppet-create_resources
Requires: puppet-drbd
Requires: puppet-firewall
Requires: puppet-haproxy
Requires: puppet-inifile
Requires: puppet-lvm
Requires: puppet-postgresql
Requires: puppet-rabbitmq
Requires: puppet-rsync
Requires: puppet-stdlib
Requires: puppet-sysctl
Requires: puppet-vcsrepo
Requires: puppet-xinetd
Requires: puppet-etcd

# 3rdparty puppet modules
Requires: puppet-boolean
Requires: puppet-certmonger
Requires: puppet-dnsmasq
Requires: puppet-filemapper
Requires: puppet-kmod
Requires: puppet-ldap
Requires: puppet-network
Requires: puppet-nslcd
Requires: puppet-nssdb
Requires: puppet-puppi
Requires: puppet-vlan
Requires: puppet-collectd

%description
Platform puppet configuration files and manifests

%define config_dir %{_sysconfdir}/puppet
%define module_dir %{_datadir}/puppet/modules
%define local_bindir /usr/local/bin

%prep
%setup

%install
make install \
     BINDIR=%{buildroot}%{local_bindir} \
     CONFIGDIR=%{buildroot}%{config_dir} \
     MODULEDIR=%{buildroot}%{module_dir}

%files
%defattr(-,root,root,-)
%license LICENSE
%{local_bindir}
%{config_dir}
%{module_dir}
