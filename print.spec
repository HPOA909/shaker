Name:           sys-printer
Version:       	1.0
Release:        1%{?dist}
Summary:        Salt a printer qube in Qubes

License:        GPLv3+
SOURCE0:	print

%description
Salt state to implement a printer qube

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/srv/salt
cp -rv %{SOURCE0}/  %{buildroot}/srv/salt

%files
%defattr(-,root,root,-)
/srv/salt/print/*

%post
if [ $1 -eq 1 ]; then
  qubesctl state.apply print.create
  qubesctl --skip-dom0 --targets=sys-printer state.apply print.configure
fi

%postun
if [ $1 -eq 0 ]; then
  sed -i /qubes.Print/d /etc/qubes/policy.d/30-user.policy
fi

%changelog
* Sun May 15 2022 unman <unman@thirdeyesecurity.org> - 1.0
- First Build