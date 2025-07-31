import requests

ipv64_subdomain = "some.ipv64.net"
ipv64_token = "null"
ipv64_domain_token = "null"
ipv64_api_url = "https://ipv64.net/api"
ipv64_nic_url = "https://ipv64.net/nic/update"

def get_ipv64_domains():
    url = f"{ipv64_api_url}?get_domains"
    
    headers = {
        "Authorization": f"Bearer {ipv64_token}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("subdomains", []).get(ipv64_subdomain, {}).get("records", [])
    else:
        return {"error": "Failed to retrieve domains"}

def filter_ipv64_domains(domains):
    ts_domains = []
    for record in domains:
        if record.get("praefix").endswith("ts"):
            ts_domains.append(record)
    
    return ts_domains

def generate_domain_json():
    domains = get_ipv64_domains()
    domains = filter_ipv64_domains(domains)
    
    output = {}

    for record in domains:
        praefix = record['praefix']
        ip_type = 'ipv4' if record['type'] == 'A' else 'ipv6'
        
        if praefix not in output:
            output[praefix] = {'ipv4': {'ip': None, 'id': None}, 'ipv6': {'ip': None, 'id': None}}

        output[praefix][ip_type]['ip'] = record['content']
        output[praefix][ip_type]['id'] = record['record_id']

    return output

def delete_ipv64_domain(list):
    url = f"{ipv64_api_url}"

    for record_id in list:
        payload = f"del_record={record_id}"
        headers = {
            "Authorization": f"Bearer {ipv64_token}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.delete(url, headers=headers, data=payload)

        if response.status_code == 202:
            print(f"Deleted record with ID: {record_id}")
        else:
            print(f"Failed to delete record with ID: {record_id}, Status Code: {response.status_code}, Response: {response.text}")

def create_ipv64_domain(machine, ips):
    name = machine + ".ts"
    ipv4 = ips['ipv4']
    ipv6 = ips['ipv6']

    url = f"https://ipv64.net/nic/update?token={ipv64_domain_token}&praefix={name}&domain={ipv64_subdomain}&ipv4={ipv4}" #&ipv6={ipv6}"

    response = requests.get(url)
    if response.status_code == 200:
        print(f"Created domain for {name} with IPv4: {ipv4} and IPv6: {ipv6}")
    else:
        print(f"Failed to create domain for {name}, Status Code: {response.status_code}, Response: {response.text}")

    return