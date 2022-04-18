# Deployment Groups

## Summary

Deployment groups can be used to group a set of hosts in a kit to enable a staggered deployment model. The hosts in a deployment group can all belong to a single site or can be made up of different hosts across several sites.

This is implemented using a host fact named `deployment_group`.

The value of this fact is not enforced so can be customised to your needs.

Some suggestions are

- `prod_1`, `prod_2`, `prod_3`, etc.. and then deploy to one group at a time.
- `staging_1`, `dev_1`, etc.. for staging and test sites.

## Examples

### All hosts from site in deployment group

In this example all hosts in the `ldn` site belong to one deployment group and all hosts in the `nyc` site belong to another.

```python
# demo-kit/datatree/sites/ldn/common.py

deployment_group = "prod_1"
```

```python
# demo-kit/datatree/sites/nyc/common.py

deployment_group = "prod_2"
```

### Specific hosts in deployment group

In this example the `firewall1.ldn` host belongs to a deployment group and `switch1.nyc` host belongs to another.

?> Note that this would override the deployment group for these individual hosts if a site has a common `deployment_group` value defined.</br>
This can be useful to mark critical hosts which should be deployed last.

```python
# demo-kit/datatree/sites/ldn/hosts/firewall1.py

deployment_group = "prod_3"  # deploy after prod_1 and prod_2
```

```python
# demo-kit/datatree/sites/nyc/hosts/switch1.py

deployment_group = "lab_1"
```
