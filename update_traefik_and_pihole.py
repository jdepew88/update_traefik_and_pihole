import sys
import yaml
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
PIHOLE_API_TOKEN = os.getenv("PIHOLE_API_TOKEN")
PIHOLE_SERVER_URL = os.getenv("PIHOLE_SERVER_URL")
DOMAIN_NAME = os.getenv("DOMAIN_NAME")
CONFIG_FILE_PATH = os.getenv("CONFIG_FILE_PATH")

def add_cname_record_to_pihole(api_token, cname_name, cname_target):
    url = PIHOLE_SERVER_URL

    data = {
        "list": "local",
        "name": cname_name,
        "target": cname_target,
        "auth": api_token
    }
    
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        print(f"Successfully added CNAME record: {cname_name} -> {cname_target}")
    elif response.status_code == 409:
        print(f"CNAME record already exists: {cname_name} -> {cname_target}")
    else:
        print(f"Failed to add CNAME record: {response.status_code} - {response.text}")

# Ensure the script is executed with a config file path argument
if CONFIG_FILE_PATH is None:
    print("Config file path is not set in the .env file.")
    sys.exit(1)

# Load the existing dynamic config from the specified config file
with open(CONFIG_FILE_PATH, 'r') as file:
    config = yaml.safe_load(file)

# Create backups directory if it doesn't exist
backup_dir = './backups'
os.makedirs(backup_dir, exist_ok=True)

# Create a backup of the current config file with a timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = os.path.join(backup_dir, f"config_backup_{timestamp}.yml")
with open(backup_file, 'w') as file:
    yaml.dump(config, file)

print(f"Backup of the original config file saved as {backup_file}")

# Get input from the user
service_name = input("Enter the name of your service: ")
ip_address = input(f"Enter the IP address of {service_name}: ")
scheme = input("Enter the scheme (http or https) for the service: ").strip().lower()

# Validate scheme input
if scheme not in ['http', 'https']:
    print("Invalid scheme. Please enter 'http' or 'https'.")
    sys.exit(1)

# Create the new router entry
router_entry = {
    service_name: {
        'entryPoints': ['https'],
        'rule': f'Host(`{service_name}.{DOMAIN_NAME}`)',
        'middlewares': ['chain-no-auth'],
        'tls': {
            'options': 'default'
        },
        'service': f'{service_name}-svc'
    }
}

# Create the new service entry
service_entry = {
    f'{service_name}-svc': {
        'loadBalancer': {
            'servers': [{'url': f'{scheme}://{ip_address}/'}],
            'passHostHeader': True
        }
    }
}

# Insert the new router entry in alphabetical order
routers = config['http']['routers']
routers.update(router_entry)
config['http']['routers'] = dict(sorted(routers.items()))

# Insert the new service entry in alphabetical order
services = config['http']['services']
services.update(service_entry)
config['http']['services'] = dict(sorted(services.items()))

# Save the updated config file, overwriting the original config.yml
with open(CONFIG_FILE_PATH, 'w') as file:
    yaml.dump(config, file)

print(f"Updated config file saved as {CONFIG_FILE_PATH}")

# Add the CNAME record to Pi-hole, pointing to the main domain
add_cname_record_to_pihole(PIHOLE_API_TOKEN, f"{service_name}.{DOMAIN_NAME}", DOMAIN_NAME)
