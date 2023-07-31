# CiberC L3VPN Management Multivendor With Idempotencia and Notify

Project to automatically deploy L3VPN in a multivendor environment, with the ability to send notifications to WebexTeams through a Bot.

# Technology stack

# Status

There is only one version that has been tested and validated in an emulated environment (EVE-NG with a multivendor ISP topology).

Currently, the project has the ability to send notifications to WebexTeams once a registered command has been completed.


# Idempotencia (Configs)

## Complete

## Partial

***

# Use Case Description

# Install

```
python3 -m pip install ciberc-l3vpn
```

# Steps to install in Ubuntu workstation (automation station)


# Configuration

## Environment Variables

```
export WEBEX_ACCESS_TOKEN=xxxxxxx
export LIST_USER_NOTIFY=xxxxxxx
```

`WEBEX_ACCESS_TOKEN`: Token generated when registering a Bot in WebexTeams Cisco.

`LIST_USER_NOTIFY`: Each email will be separated by `,`

## Inventory



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

# Usage

# configuration example

# How to test the software

# Getting help

# Link Video Example
