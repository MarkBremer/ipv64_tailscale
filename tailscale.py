import requests
import json

ts_token = "tskey-api-null"
ts_tailnet = "null.ts.net"
ts_api_url = "https://api.tailscale.com/api/v2"

def get_ts_devices():
    url = f"{ts_api_url}/tailnet/{ts_tailnet}/devices"
    
    headers = {
        "Authorization": f"Bearer {ts_token}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("devices", [])
    else:
        return {"error": "Failed to retrieve Tailscale devices"}
    
def generate_device_json():
    devices = get_ts_devices()
    
    output = {}

    for device in devices:
        name = device['name'].split('.')[0]
        ipv4 = device.get('addresses', [])[0] if device.get('addresses') else None
        ipv6 = device.get('addresses', [])[1] if len(device.get('addresses', [])) > 1 else None
        
        output[name] = {'ipv4': ipv4, 'ipv6': ipv6}

    return output