# Cloud Deployment Project – Compute Engine VM Automation

## Project Overview
This project automates the deployment of a Google Cloud Compute Engine Virtual Machine with the following specifications:
- **Machine Type:** At least 2 vCPUs and 8GB RAM (using machine type: `e2-standard-2`)
- **Storage:** 250GB boot disk
- **Image:** Ubuntu 20.04 (Ubuntu 20.04 LTS)
- **Static IP:** A reserved external static IP address is attached to the VM.
- **Firewall:** A firewall rule is configured to allow HTTP (port 80) and SSH (port 22) access.

## Prerequisites
Before running the deployment script, ensure you have the following:
- **Google Cloud SDK:** Installed on your machine.  
  Installation guide: [Google Cloud SDK Installation](https://cloud.google.com/sdk/docs/install)
- **Google Cloud Project:** An active project with billing enabled.
- **Enabled APIs:** Compute Engine API and IAM API must be enabled in your project.
- **IAM Permissions:** Your account should have sufficient permissions (e.g., Project Owner, Editor, or Service Usage Admin).
- **Python 3.x:** Installed and added to your system PATH. Download from [Python.org](https://www.python.org/downloads/).
- **Required Python Packages:** Install them using:
  ```bash
  python -m pip install google-api-python-client google-auth


## Authentication
### Setup Application Default Credentials by running: 
gcloud auth application-default login

## Guidelines for Executing the Script
### The repository is cloned by using the command : 
git clone https://github.com/Snehith4reddy/cloud-deployment-project1.git
cd cloud-deployment-project1

### Update The Script 
open the file deploy.py in a text editor

### Run the Deployment Script
python deploy.py

## Examine the Results:

 The script will set up a firewall rule, create a virtual machine, and reserve a static IP.

 "Reserved static IP address: [STATIC_IP]", "VM instance created.", "Firewall rule created.", and "Deployment complete." are examples of console messages that should validate each step.

## Anticipated Results
 Terminal Output:  You ought to see confirmation messages:

 IP reservation that is static

 creation of a virtual machine instance

 Configuring firewall rules

## Google Cloud Console:
 Your virtual machine (VM), such as my-vm-instance, should be visible and operational under Compute Engine > VM instances.

 Access via SSH:  To access your virtual machine, use:
 gcloud compute ssh my-vm-instance --zone=us-central1-a

 HTTP Access: Open a web browser and navigate to:
 http://<STATIC_IP>

 If Apache or your preferred web server is set up properly, you ought to see a "Hello World" page.


## Troubleshooting
### Not Enabled Compute Engine API:
 If you encounter an API error, either run the following commands or enable it through the Cloud Console:
 gcloud services enable compute.googleapis.com --project=YOUR_PROJECT_ID
 ### Billing Issues:
 Ensure your project has an active billing account.

 ### Authentication Errors:
 Re-run:
 gcloud auth application-default login

 ### Static IP Not Found:
 Use:gcloud compute addresses list

 
