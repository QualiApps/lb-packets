# IoT LB
Initialize keepalived + LVS-DR + consul-template

## How to install

### Pre-install

####Define env var

`CONSUL_ADDR - consul ip-address`
`CONSUL_PORT - consul port. Default: 8500`
`INTERFACE - vrrp section interface. Default: eth0`
`STATE - vrrp section state. Default: MASTER`
`PRIORITY - vrrp section priority. Default: 100`
`VIRTUAL_IP - floating ip. Default: 192.168.1.100`

### Install package

`dpkg -i DEB_PACKAGE`
`apt-get update & -f install`
