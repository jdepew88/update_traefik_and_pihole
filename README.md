
# Automated Traefik Service Configuration and Pi-hole CNAME Management

## Description
This project automates the addition of services to Traefik's dynamic configuration and updates Pi-hole for local DNS resolution. Designed for use on an Unraid server or a Docker Compose setup, it ensures seamless internal accessibility and SSL support for services by modifying the Traefik v2 dynamic configuration file and utilizing Pi-hole's API.

## Features
### Automated Service Configuration:
- Adds and updates services (router/service) in Traefik's `config.yml` dynamically.
- Supports SSL and efficient routing of internal services.

### Automated CNAME Management:
- Adds CNAME records to Pi-hole for local DNS resolution.

## Usage
This script simplifies the process by asking three questions:
1. **Service name:** The subdomain name for the service (e.g., entering `plex` will resolve to `plex.local.mydomain.com`).
2. **Local IP address and port:** (Example for Plex: `10.10.0.100:32400`).
3. **Scheme:** Whether the service resolves with HTTP or HTTPS.

## How It Works
### Internal Access:
- Updates Traefik's configuration to route services internally.
- Utilizes Pi-hole for local DNS resolution, ensuring services are accessible via `servicename.local.mydomain.com` with CNAME records pointing to `local.mydomain.com`.

This project ensures efficient internal service management with minimal manual intervention, tailored specifically for environments using Traefik and Pi-hole.

## How to Set Up
### Clone the Repository:
````sh
git clone https://github.com/yourusername/yourrepository.git
````

### Extract Files:
Extract the `.env` file and the two scripts (`setup_and_run.sh` and `update_traefik_and_pihole.py`) to the Traefik folder.
- **For Unraid:**
```` sh
mv .env setup_and_run.sh update_traefik_and_pihole.py /mnt/user/appdata/traefik/
````
- **For Docker Compose:**
```` sh
mv .env setup_and_run.sh update_traefik_and_pihole.py /opt/appdata/traefik/
````

### Configure .env File:
```` env
PIHOLE_API_TOKEN=your_pihole_api_token
PIHOLE_SERVER_URL=http://10.10.10.10/admin/api.php
DOMAIN_NAME=local.mydomain.com
CONFIG_FILE_PATH=/mnt/user/appdata/traefik/config.yml
````

### Make the Shell Script Executable:
- **For Unraid:**
```` sh
chmod +x /mnt/user/appdata/traefik/setup_and_run.sh
````
- **For Docker Compose:**
```` sh
chmod +x /opt/appdata/traefik/setup_and_run.sh
````

### Run the Script:
Navigate to the Traefik directory and run the setup script:
- **For Unraid:**
````sh
cd /mnt/user/appdata/traefik
./setup_and_run.sh
````
- **For Docker Compose:**
````sh
cd /opt/appdata/traefik
./setup_and_run.sh
````
