def clab_mgmt():
    print("set interfaces fxp0 unit 0 family inet address 10.0.0.15/24")
    print("set interfaces fxp0 unit 0 family inet6 address 2001:db8::2/64")
    print("set system management-instance")
    print(
        "set routing-instances mgmt_junos routing-options rib mgmt_junos.inet6.0 static route ::/0 next-hop 2001:db8::1"
    )
    print(
        "set routing-instances mgmt_junos routing-options static route 0.0.0.0/0 next-hop 10.0.0.2"
    )
