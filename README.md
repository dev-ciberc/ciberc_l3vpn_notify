# CiberC L3VPN Management Multivendor With Idempotencia and Notify

Project to automatically deploy L3VPN in a multivendor environment, with the ability to send notifications to WebexTeams through a Bot. Plataforms `iosxr`, `ios`, `huawei_vrp`, `junos`

# Technology stack

Python 3.8+ or higher, Nornir 3.3.0 and Napalm 4.1.0

# Status

There is only one version that has been tested and validated in an emulated environment (EVE-NG with a multivendor ISP topology).

Currently, the project has the ability to send notifications to WebexTeams once a registered command has been completed.


# Idempotence (Configs)

The idempotence of the system will depend on the 'dry run' manually sent by the user. The user will handle the Napalm system for commits.

## Complete

This complete procedure is available for `Huawei`, `Cisco IOS XE`, and `Junos`.

## Partial

If we remember, `Cisco IOS XR` currently does not have a `Napalm Commit Confirm` process in its system. However, CiberC has created a process to provide partial DIFF support and allow for partial idempotence support with `Commit Confirm`, based on `dry run`.


https://napalm.readthedocs.io/en/latest/support/index.html#configuration-support-matrix


# Diff (Configs)

## Complete
`Huawei`, `Cisco IOS XE`, `Junos`

## Partial

`Cisco IOS XR`

***

# Use Case Description

Service providers who wish to implement L3VPN services in an automated way, with support for multi-vendor environments, can generate a standard model for service deployment using this tool. Additionally, this tool is useful for companies that already have this service and require automated configuration for multiple devices, saving time in implementation and validation. An important process in this platform is the notification system in Webex Teams.

# Install

```
python3 -m pip install ciberc-l3vpn
```

# Manual Steps to install in Ubuntu workstation (automation station)

```
git clone https://github.com/dev-ciberc/ciberc_l3vpn_notify.git
cd ciberc_l3vpn_notify

python3 -m venv .venv
source .venv/bin/activate

python3 -m pip install -r requirements.txt
bash build.sh
```


# Configuration

## Environment Variables

```
export WEBEX_ACCESS_TOKEN=xxxxxxx
export LIST_USER_NOTIFY=xxxxxxx
```

`WEBEX_ACCESS_TOKEN`: Token generated when registering a Bot in WebexTeams Cisco.

`LIST_USER_NOTIFY`: Each email will be separated by `,`

## Inventory

For the correct configuration of the inventory, we rely on two Nornir files, specifically `hosts.yaml` and `defaults.yaml`, which will be located in the root directory where the CLI program will be executed.


Example of the only variables needed for the L3VPN configuration for each file


`defaults.yaml`

```
---
data:
  local_bgp_as: "64512"
  vpn_name: "VPN-A"
  vpn_rd: "64512:65512"
  vpn_rt: "64512:65512"
  neighbor_remote_as: "65512"
```

`hosts.yaml`

```
---
REFLECTOR:
  hostname: 192.168.10.77
  port: 22
  username: user1
  password: passexample1
  platform: ios
  data:
    - 

PE1:
  hostname: 192.168.10.11
  port: 22
  username: user1
  password: passexample1
  platform: iosxr
  data:
    vpn_int_ip: "192.168.10.2"
    vpn_int_mask: "/30"
    interface_connect_CE: "GigabitEthernet0/0/0/0"
    vpn_bpg_ce_neighbor_ip: "192.168.10.1"
    
PE4:
  hostname: 192.168.10.44
  port: 22
  username: user1
  password: passexample1
  platform: ios
  data:
    vpn_int_ip: "192.168.40.2"
    vpn_int_mask: "255.255.255.252"
    interface_connect_CE: "GigabitEthernet2"
    vpn_bpg_ce_neighbor_ip: "192.168.40.1"
    
PE5:
  hostname: 192.168.10.55
  port: 22
  username: user1
  password: passexample1
  platform: junos
  data:
    vpn_int_ip: "192.168.50.2"
    vpn_int_mask: "/30"
    interface_connect_CE: "em1"
    vpn_bpg_ce_neighbor_ip: "192.168.50.1"
    
PE6:
  hostname: 192.168.10.66
  port: 22
  username: user2
  password: passexample2
  platform: huawei_vrp
  data:
    vpn_int_ip: "192.168.60.2"
    vpn_int_mask: "255.255.255.252"
    interface_connect_CE: "Ethernet1/0/2"
    vpn_bpg_ce_neighbor_ip: "192.168.60.1"
```

# Supported platforms

`iosxr`

`ios`

`huawei_vrp`

`junos`


# Examples

## Command L3VPN Configure

This command configures L3VPN for one or all devices.

Example for specific devices:

```
ciberc-l3vpn configure --device=PE1
```

```python
(.venv) ➜  ciberc_l3vpn_notify git:(main) ✗ ciberc-l3vpn configure --device=PE1
Configuring L3VPN
---- PE1: Diff, =>PARTIAL support<= for IOS-XR ** changed : False -------------- INFO
+   64512:65512
+   64512:65512
+  ipv4 address 192.168.10.2/30
+  no shutdown
+ router bgp 64512
+   address-family vpnv4 unicast
+   vrf VPN-A
+    rd 64512:65512
+    address-family ipv4 unicast
+    !
+    neighbor 192.168.10.1
+      remote-as 65512
+      address-family ipv4 unicast
+       route-policy Policy-PASS in
+       route-policy Policy-PASS out
+       as-override
+       commit
+     !
+    !
+ !
```

Example for all devices  `all`:

```
ciberc-l3vpn configure --device=all
```


## Command L3VPN Rollback

```
ciberc-l3vpn rollback --device=PE1,PE2
```

```bash
(.venv) ➜  ciberc_l3vpn_notify git:(main) ciberc-l3vpn rollback --device=PE1                                         
Configuring L3VPN
2it [00:11,  5.57s/it]
```

## Command L3VPN Reflector

The reflector will show us which devices are being announced and which are not, validating which devices have been configured correctly.

```
ciberc-l3vpn reflector
```

```bash
Reflector L3VPN
---- REFLECTOR: _report_bgp_neighbors ** changed : False ----------------------- INFO
[ ('1.1.1.1', '4', '64512', '47186', '52292', '1010', '0', '0', '4w4d', '4'),
  ('2.2.2.2', '4', '64512', '47235', '52533', '1010', '0', '0', '4w4d', '0'),
  ('3.3.3.3', '4', '64512', '47177', '52249', '1010', '0', '0', '4w4d', '4'),
  ('4.4.4.4', '4', '64512', '45754', '46067', '1010', '0', '0', '4w0d', '5'),
  ('5.5.5.5', '4', '64512', '86221', '84691', '1010', '0', '0', '3w5d', '4'),
  ('6.6.6.6', '4', '64512', '35473', '34121', '1010', '0', '0', '3w0d', '4')]
```

# Structure


```bash
├── ciberc_l3vpn_notify
│   ├── configure.py
│   ├── core.py
│   ├── __init__.py
│   ├── main.py
│   ├── notify.py
│   ├── reflector.py
│   ├── rollback.py
│   └── templates
│       ├── config-templates
│       │   ├── huawei_vrp.j2
│       │   ├── ios.j2
│       │   ├── iosxr.j2
│       │   └── junos.j2
│       └── rollback-templates
│           ├── huawei_vrp.j2
│           ├── ios.j2
│           ├── iosxr.j2
│           └── junos.j2
```

# Usage

# configuration example

# How to test the software

# Getting help

# Link Video Example
