%define _prefix /var/lib/mmsagent


Name:		mms-backup-agent
Group:		System Environment/Daemons
Version:	20131118.0
Release:	1%{?dist}
Summary:	10gen MongoDB Backup Agent
License:	Proprietary
Source:		mms-backup-agent-linux_amd64.tar.gz
Source1:	mms-backup-agent.service
NoSource:	0
Requires(pre):	systemd
Requires:	mms-agent

%description
%{summary}

%prep
%setup -q -n backup-agent %{SOURCE}

%build

%install
%__install -d "%{buildroot}%{_prefix}"
%__install -d "%{buildroot}%{_prefix}/backup-agent"
cp -p $RPM_BUILD_DIR/backup-agent/* "%{buildroot}%{_prefix}/backup-agent/"
%__install -d %{buildroot}/usr/lib/systemd/system/
%__install -D -m0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/mms-backup-agent.service

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,mmsagent,mmsagent,-)
%doc /var/lib/mmsagent/backup-agent/README
/var/lib/mmsagent/backup-agent/backup-agent
%config  /var/lib/mmsagent/backup-agent/local.config
%attr(0644,root,root) /usr/lib/systemd/system/mms-backup-agent.service

%preun
if [ $1 = 0 ] ; then
	systemctl stop mms-backup-agent.service
	systemctl disable mms-backup-agent.service
fi

%postun
if [ "$1" -ge "1" ] ; then
	systemctl reload-or-restart mms-backup-agent.service
fi

%post
systemctl enable mms-backup-agent.service
systemctl start mms-backup-agent.service

%changelog
* Tue Nov 19 2013 Scott Rossillo <scott@rossillo.net>
- Upgraded agent to v20131118.0

* Sun Oct 07 2013 Scott Rossillo <scott@rossillo.net>
- Initial release

