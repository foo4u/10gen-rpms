%define _prefix /var/lib/mmsagent


Name:		mms-agent
Version:	1.5.9
Release:	1%{?dist}
Summary:	10gen MongoDB Monitoring Agent
License:	Proprietary
Source:		https://mms.mongodb.com/settings/mms-monitoring-agent.tar.gz
Source1:	mms-agent.service
Requires(pre):	systemd
Requires:	python-pymongo

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

%preun
if [ $1 = 0 ] ; then
	systemctl stop  mmsagent.service
	systemctl disable mmsagent.service
fi

%postun
if [ "$1" -ge "1" ] ; then
	systemctl reload-or-restart mmsagent.service
fi

%post
systemctl enable mmsagent.service
systemctl start mmsagent.service

