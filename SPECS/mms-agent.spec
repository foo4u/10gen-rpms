%define _prefix /var/lib/mmsagent


Name:		mms-agent
Group:		System Environment/Daemons
Version:	1.6.4
Release:	2%{?dist}
Summary:	10gen MongoDB Monitoring Agent
License:	Proprietary
Source:		https://mms.mongodb.com/settings/mms-monitoring-agent.tar.gz
Source1:	mms-agent.service
NoSource:	0
Requires(pre):	systemd
Requires:	python-pymongo >= 1.9

%description
%{summary}

%prep
%setup -q -n mms-agent mms-monitoring-agent.tar.gz

%build

%install
%__install -d "%{buildroot}%{_prefix}"
%__install -d "%{buildroot}%{_prefix}/mms-agent"
cp -p $RPM_BUILD_DIR/mms-agent/*py "%{buildroot}%{_prefix}/mms-agent"
cp -p $RPM_BUILD_DIR/mms-agent/README "%{buildroot}%{_prefix}/mms-agent"
%__install -d %{buildroot}/usr/lib/systemd/system/
%__install -D -m0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,mmsagent,mmsagent,-)
%doc /var/lib/mmsagent/mms-agent/README
/var/lib/mmsagent/mms-agent/agent.py
/var/lib/mmsagent/mms-agent/agentProcess.py
/var/lib/mmsagent/mms-agent/blockingStats.py
/var/lib/mmsagent/mms-agent/confPull.py
/var/lib/mmsagent/mms-agent/getLogs.py
/var/lib/mmsagent/mms-agent/mmsAgent.py
/var/lib/mmsagent/mms-agent/munin.py
/var/lib/mmsagent/mms-agent/nonBlockingStats.py
/var/lib/mmsagent/mms-agent/pymongotest.py
/var/lib/mmsagent/mms-agent/pythonversiontest.py
%config   /var/lib/mmsagent/mms-agent/logConfig.py
%config  /var/lib/mmsagent/mms-agent/settings.py
%attr(0644,root,root) /usr/lib/systemd/system/mms-agent.service

%pre
getent group mmsagent >/dev/null || groupadd -r mmsagent
getent passwd mmsagent >/dev/null || useradd -g mmsagent -r -c "MongoDB Monitoring Agent" -m -d %{_prefix} mmsagent

%preun
if [ $1 = 0 ] ; then
	systemctl stop  mms-agent.service
	systemctl disable mms-agent.service
fi

%postun
if [ "$1" -ge "1" ] ; then
	systemctl reload-or-restart mms-agent.service
fi

%post
systemctl enable mms-agent.service
systemctl start mms-agent.service

%changelog
* Tue Nov 19 2013 Scott Rossillo <scott@rossillo.net>
- Upgraded agent to 1.6.4

* Mon Oct 07 2013 Scott Rossillo <scott@rossillo.net>
- Upgraded agent to 1.6.0
- Added useradd for mmsagent


