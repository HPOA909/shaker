# vim: set syntax=yaml ts=2 sw=2 sts=2 et :
#
#
#

{% if grains['nodename'] == 'dom0' %}

/var/lib/qubes/vm-kernels/mirage-firewall:
  file.directory:
    - mode: 755
    - makedirs: True

mirage_extracted:
  archive.extracted:
    - name: /var/lib/qubes/vm-kernels/
    - source: salt://mirage/mirage-firewall.tar.bz2
    - source_hash: 2c985671a5620f395d1cc40f7f505660fd1e07bcaaaf77f698ce13f76f47cc20
    - archive_format: tar
    - options: -j

mirage-firewall:
  qvm.present:
    - name: mirage-firewall
    - class: StandaloneVM
    - label: green
    - virt_mode: pvh
    - kernel: mirage-firewall
    - kernelopts: ''
    - mem: 32
    - vcpus: 1

mirage-firewall-prefs:
  qvm.prefs:
    - name: mirage-firewall
    - kernel: mirage-firewall
    - maxmem: 32
    - provides-network: True
    - netvm: sys-net
    - default_dispvm: ''

mirage-firewall-features:
  qvm.features:
    - name: mirage-firewall
    - enable:
      - qubes-firewall
      - no-default-kernelopts


{% endif %}
