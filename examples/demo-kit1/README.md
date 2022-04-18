# Juniper 2 site kit

This nectl kit is an example which contains a bit of all the functionality commonly seen in a kit.

?> Before trying this kit it is highly recommended that you read through the guide in the docs site.

## Dependencies

This kit requires

- nectl
- pydantic

## Sites and Hosts

There are 2 sites each with 2 hosts.

- site: **ldn**
  - host: **firewall1**
  - host: **router1**
- site: **nyc**
  - host: **firewall1**
  - host: **router1**

## Data Models

- Data models have been created for routed interfaces and BGP neighbors.

## Facts

### Host definitions

- The firewall hosts are defined as a single file.
- The router hosts are defined as a directory with several files.

### DNS

- DNS servers are configured at the global common level.

### NTP

- NTP servers are configured at the site common level.

### SNMP

- SNMP auth is configured at the global common level and cannot be modified.
- SNMP clients are configured at the global and site common level.

### Roles

- There are roles for `router` and `firewall` used to set the login message.

## Templates

- There is a template for the `junos` OS with several sub-templates.
