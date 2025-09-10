def check_ssh_access(napalm_driver):
    # GIVEN napalm host
    napalm_driver

    # WHEN checking if device is alive
    is_alive = napalm_driver.is_alive()

    # THEN expect True
    assert is_alive


def check_hostname(host, napalm_driver):
    # GIVEN hostname
    hostname = host.id  # host.id is {hostname}.{site}

    # WHEN getting live host facts
    facts = napalm_driver.get_facts()

    # THEN expect actual hostname to match
    assert facts.get("hostname") == hostname
