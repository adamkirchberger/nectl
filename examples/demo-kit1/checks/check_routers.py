__hosts_filter__ = lambda host: host.role == "router"


def check_interfaces(host, napalm_driver):
    # GIVEN datatree interfaces
    datatree_interfaces = host.interfaces

    # GIVEN live host interfaces
    live_interfaces = napalm_driver.get_interfaces()

    # WHEN looping through each interface
    for iface_name, iface in datatree_interfaces.items():
        live_interface = live_interfaces[iface_name]

        # THEN expect interface to be up and enabled
        assert live_interface.get("is_up")
        assert live_interface.get("is_enabled")
