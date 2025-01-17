Name:           3isec-qubes-sys-vpn
Version:       	1.4
Release:        1%{?dist}
Summary:        Create an openvpn proxy in Qubes

License:        GPLv3+
SOURCE0:	      openvpn

%description
This package sets up a VPN gateway, named sys-vpn, using openvpn.
It follows the method detailed in the Qubes docs,
 https://github.com/Qubes-Community/Contents/blob/master/docs/configuration/vpn.md
using iptables and CLI scripts.

The package creates a qube called sys-vpn based on the debian-11-minimal
template.  If the debian-11-minimal template is not present, it will
be downloaded and installed - this may take some time depending on your
net connection.

There are minor changes to the firewall rules on sys-vpn to ensure
blocking of outbound connections.

After installing, copy your openvpn configuration file or zip file
to sys-vpn.
Run setup_vpn to set up the VPN. 
There should be a menu item for this script - if you cannot see it, you may
need to refresh the application list in sys-vpn settings.
When finished, restart sys-vpn.

To use the VPN, set sys-vpn as the netvm for your qubes(s).
All traffic will go through the VPN.
The VPN will fail closed if the connection drops.
No traffic will go through clear.

If you remove the package, the salt files will be removed.
**The sys-vpn gateway will also be removed.**
To do this ALL qubes will be checked to see if they use sys-vpn.
If they do, their netvm will be set to `none`.

You can, of course, use template-openvpn to create other VPN gateways.


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/srv/salt
cp -rv %{SOURCE0}/  %{buildroot}/srv/salt

%files
%defattr(-,root,root,-)
/srv/salt/openvpn/*

%post
if [ $1 -eq 1 ]; then
  qubesctl state.apply openvpn.clone
  qubesctl --skip-dom0 --targets=template-openvpn state.apply openvpn.install
  qubesctl state.apply openvpn.create
  qubesctl --skip-dom0 --targets=sys-vpn state.apply openvpn.client_install
fi

%postun
if [ $1 -eq 0 ]; then
  for i in `qvm-ls -O NAME,NETVM | awk '/ sys-vpn/{ print $1 }'`;do qvm-prefs $i netvm none; done
  qvm-kill sys-vpn
  qvm-remove --force sys-vpn template-openvpn 
fi

%changelog
* Mon Jun 12 2023 unman <unman@thirdeyesecurity.org> - 1.4
- Fix typo
* Mon Feb 20 2023 unman <unman@thirdeyesecurity.org> - 1.3
- Use pillar for cacher to determine repo changes
* Thu Sep 29 2022 unman <unman@thirdeyesecurity.org> - 1.2
- Force creation of menu item for setup script.
* Sat Sep 17 2022 unman <unman@thirdeyesecurity.org> - 1.1
- Change in menu creation for setup item.
- Improve description.
* Wed May 18 2022 unman <unman@thirdeyesecurity.org> - 1.0
- First Build
