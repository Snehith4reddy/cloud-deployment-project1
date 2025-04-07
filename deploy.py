import time
from googleapiclient import discovery
from google.auth import default

def wait_for_zone_operation(service, project, zone, operation):
    """Poll a zone-level operation until it completes."""
    print("Waiting for zone operation to finish...")
    while True:
        result = service.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation['name']
        ).execute()
        if result['status'] == 'DONE':
            print("Zone operation finished.")
            if 'error' in result:
                raise Exception(result['error'])
            return result
        time.sleep(1)

def wait_for_region_operation(service, project, region, operation):
    """Poll a region-level operation until it completes."""
    print("Waiting for region operation to finish...")
    while True:
        result = service.regionOperations().get(
            project=project,
            region=region,
            operation=operation['name']
        ).execute()
        if result['status'] == 'DONE':
            print("Region operation finished.")
            if 'error' in result:
                raise Exception(result['error'])
            return result
        time.sleep(1)

def wait_for_global_operation(service, project, operation):
    """Poll a global operation until it completes."""
    print("Waiting for global operation to finish...")
    while True:
        result = service.globalOperations().get(
            project=project,
            operation=operation['name']
        ).execute()
        if result['status'] == 'DONE':
            print("Global operation finished.")
            if 'error' in result:
                raise Exception(result['error'])
            return result
        time.sleep(1)

def main():
    
    project = 'cloud-deployment-project1'          
    zone = 'us-central1-a'               # The zone where the VM will be deployed
    region = zone.rsplit('-', 1)[0]        # Derive region from zone (e.g., 'us-central1')
    instance_name = 'my-vm-instance'       # Desired VM instance name
    machine_type = f"zones/{zone}/machineTypes/e2-standard-2"  # 2 vCPUs, 8GB RAM
    source_image = "projects/ubuntu-os-cloud/global/images/family/ubuntu-2004-lts"
    disk_size_gb = "250"                 # Boot disk size in GB
    static_ip_name = 'my-vm-ip'           # Name for the reserved static IP
    firewall_rule_name = 'allow-http-ssh' # Name for the firewall rule

    # Authenticate and build the Compute Engine service object.
    credentials, _ = default()
    compute = discovery.build('compute', 'v1', credentials=credentials)

    # -------------------------------
    # Reserve a static external IP address.
    # -------------------------------
    print("Reserving a static IP address...")
    address_body = {
        'name': static_ip_name
    }
    operation = compute.addresses().insert(
        project=project,
        region=region,
        body=address_body
    ).execute()
    wait_for_region_operation(compute, project, region, operation)

    # Retrieve the reserved IP address.
    address_result = compute.addresses().get(
        project=project,
        region=region,
        address=static_ip_name
    ).execute()
    static_ip = address_result['address']
    print(f"Reserved static IP address: {static_ip}")

    # -------------------------------
    # Create the Compute Engine VM instance.
    # -------------------------------
    print("Creating the VM instance...")
    instance_config = {
        'name': instance_name,
        'machineType': machine_type,
        'disks': [{
            'boot': True,
            'autoDelete': True,
            'initializeParams': {
                'sourceImage': source_image,
                'diskSizeGb': disk_size_gb,
            }
        }],
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [{
                'name': 'External NAT',
                'type': 'ONE_TO_ONE_NAT',
                'natIP': static_ip
            }]
        }],
        'tags': {
            'items': ['http-server', 'https-server']
        }
    }
    operation = compute.instances().insert(
        project=project,
        zone=zone,
        body=instance_config
    ).execute()
    wait_for_zone_operation(compute, project, zone, operation)
    print("VM instance created.")

    # -------------------------------
    # Creating a firewall rule to allow HTTP (port 80) and SSH (port 22) access.
    # -------------------------------
    print("Creating firewall rule...")
    firewall_body = {
        'name': firewall_rule_name,
        'allowed': [
            {'IPProtocol': 'tcp', 'ports': ['80']},
            {'IPProtocol': 'tcp', 'ports': ['22']}
        ],
        'targetTags': ['http-server', 'https-server'],
        'direction': 'INGRESS',
        'sourceRanges': ['0.0.0.0/0']
    }
    operation = compute.firewalls().insert(
        project=project,
        body=firewall_body
    ).execute()
    wait_for_global_operation(compute, project, operation)
    print("Firewall rule created.")

    print("Deployment complete.")

if __name__ == '__main__':
    main()
