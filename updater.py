import time
import requests
import json

from ipv64      import *
from tailscale  import generate_device_json

"""
Filter IPv64 domains not in Tailscale devices
These domains will be deleted.
"""
def filter_ipv64_domains_not_in_tailscale(ipv64_domains, ts_devices):
    filtered_domains = []
    
    for domain in ipv64_domains:
        ipv4_id = ipv64_domains[domain]['ipv4']['id']
        ipv6_id = ipv64_domains[domain]['ipv6']['id']

        if domain == "ts":
            continue

        if domain.split('.')[0] not in ts_devices:
            if ipv4_id is not None:
                filtered_domains.append(ipv4_id)
            if ipv6_id is not None:
                filtered_domains.append(ipv6_id)

    return filtered_domains

"""
Filter Tailscale devices not in IPv64 domains
These devices will be created.
"""
def filter_tailscale_devices_not_in_ipv64(ipv64_domains, ts_devices):
    filtered_devices = {}
    
    for device in ts_devices:
        name = device.split('.')[0]
        ipv4 = ts_devices[device]['ipv4']
        ipv6 = ts_devices[device]['ipv6']

        filtered_devices[name] = {'ipv4': ipv4, 'ipv6': ipv6}

        continue
    return filtered_devices



# main function
if __name__ == "__main__":
    ipv64_domains   = generate_domain_json()
    ts_devices      = generate_device_json()

    delete_domains  = filter_ipv64_domains_not_in_tailscale(ipv64_domains, ts_devices)
    create_domains  = filter_tailscale_devices_not_in_ipv64(ipv64_domains, ts_devices)

    delete_ipv64_domain(delete_domains)

    for machine in create_domains:
        create_ipv64_domain(machine, create_domains[machine])
        time.sleep(3.35)

    exit(0)