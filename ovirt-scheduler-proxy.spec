#
# Copyright 2013 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Enable/disable features according to the type of distribution:
%if 0%{?fedora}
%global install_systemd 1
%global install_systemv 0
%endif

%if 0%{?rhel}
%global install_systemd 0
%global install_systemv 1
%endif

Name: ovirt-scheduler-proxy
Version: 0.1.1
Release: 1%{?dist}
Summary: Scheduling Proxy for Open Virtualization
Group: Virtualization/Management
License: ASL 2.0
URL: http://www.ovirt.org
Source: http://ovirt.org/releases/stable/src/%{name}-%{version}.tar.gz
BuildArch: noarch

%if %{install_systemd}
BuildRequires: systemd
%endif

Requires: python


%description
The scheduler proxy runs user defined scripts to filter and fine-tune
load-balancing of their oVirt system.


%prep
%setup -q


%build
%{__python} setup.py \
    build


%install

# Install the python files:
%{__python} setup.py \
    install \
    -O1 \
    --skip-build \
    --root %{buildroot}

# Install the systemd service file:
%if %{install_systemd}
install \
    -dm 755 \
    %{buildroot}%{_unitdir}
install \
    -m 644 \
    packaging/ovirt-scheduler-proxy.systemd \
     %{buildroot}%{_unitdir}/ovirt-scheduler-proxy.service
%endif

# Install the System V init script:
%if %{install_systemv}
install \
    -dm 755 \
    %{buildroot}%{_initddir}
install \
    -m 755 \
    packaging/ovirt-scheduler-proxy.sysv \
     %{buildroot}%{_initddir}/ovirt-scheduler-proxy
%endif

# Install the data directory:
install \
    -dm 755 \
    %{buildroot}%{_datadir}/ovirt-scheduler-proxy

# Install the directory for plugins:
install \
    -dm 755 \
    %{buildroot}%{_datadir}/ovirt-scheduler-proxy/plugins

# Install the directory for logs:
install \
    -dm 755 \
    %{buildroot}%{_localstatedir}/log/ovirt-scheduler-proxy


%pre

# Create the user if it doesn't exist:
getent group ovirt &>/dev/null || \
    groupadd \
        -g 108 \
        ovirt

# Create the group if it doesn't exist:
getent passwd ovirt &>/dev/null || \
    useradd \
        -u 108 \
        -g ovirt \
        -c "oVirt Manager" \
        -s /sbin/nologin \
        -d %{_datadir}/ovirt-scheduler-proxy \
        ovirt


%post

# Make sure that systemd reloads its configuration once the package is
# installed, otherwise it won't recognize the new service name:
%if %{install_systemd}
%systemd_post ovirt-scheduler-proxy.service
%endif

# Register the service:
%if %{install_systemv}
chkconfig --add ovirt-scheduler-proxy
%endif


%postun

# Make sure that the service is stoped and removed from the systemd
# configuration:
%if %{install_systemd}
%systemd_postun ovirt-scheduler-proxy.service
%endif

# Stop the SysV service only if the package is being completely
# uninstalled:
%if %{install_systemv}
if [ $1 -eq 0 ]
then
    service ovirt-scheduler-proxy stop &>/dev/null
    chkconfig --del ovirt-scheduler-proxy
fi
%endif


%files

# Python files (included the generated egg):
%{python_sitelib}/ovirtscheduler
%{python_sitelib}/ovirt_scheduler_proxy-*.egg-info

# Systemd and SysV files:
%if %{install_systemd}
%{_unitdir}/ovirt-scheduler-proxy.service
%endif
%if %{install_systemv}
%{_initddir}/ovirt-scheduler-proxy
%endif

# Data directory:
%{_datadir}/ovirt-scheduler-proxy

# Logs directory needs to be owned by the user that runs the service because it
# needs to create files inside:
%attr(-, ovirt, ovirt) %{_localstatedir}/log/ovirt-scheduler-proxy

# Documentation files:
%doc LICENSE
%doc README


%changelog
* Thu Sep 05 2013 Juan Hernandez <juan.hernandez@redhat.com> - 0.1.1-1
- Fixes in license headers to adapt them to ASL 2.0
- Added ASL 2.0 license file

* Fri Aug 09 2013 Juan Hernandez <juan.hernandez@redhat.com> - 0.1-1
- Initial packaging
