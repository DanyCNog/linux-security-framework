# Enterprise Linux Security & Compliance Framework

## Overview

This repository contains an automated DevSecOps framework designed to enforce and audit security configurations on Linux environments (Debian/Ubuntu distributions). The project is strictly aligned with industry-standard security baselines, specifically drawing inspiration from the **CIS (Center for Internet Security) Benchmarks**.

The architecture is divided into two decoupled components:
1. **Enforcement (Infrastructure as Code):** Utilizes Ansible to apply idempotent security configurations, effectively mitigating configuration drift.
2. **Validation (Compliance Scanner):** A custom Python-based auditing tool that remotely connects to target nodes, verifies the active state of security policies, and generates a structured compliance report.

## Project Architecture

The framework operates on a continuous compliance model:

- **Target Node:** A Linux server acting as the subject of the hardening procedures.
- **Control Node:** The administrative machine executing the Ansible playbooks and Python scanner via SSH public key authentication.

### Key Capabilities

- **SSH Hardening:** Disables root login and empty passwords, enforcing secure remote access policies.
- **Network Security:** Automates the installation, configuration, and activation of UFW (Uncomplicated Firewall) with a default-deny policy for incoming traffic.
- **Automated Auditing:** Programmatic verification of configuration files and systemd service states without manual intervention.

## Repository Structure

```text
linux-security-framework/
├── hardening/                  # Ansible IaC definitions
│   ├── inventory/
│   │   └── hosts.ini           # Target server definitions and connection variables
│   ├── playbooks/
│   │   └── hardening.yml       # Main playbook orchestrating the security roles
│   └── roles/
│       ├── firewall/           # UFW configuration and state management
│       └── ssh_hardening/      # SSH daemon security configurations
├── scanner/                    # Python auditing tool
│   ├── main.py                 # Core scanner logic and SSH remote execution
│   └── report/                 # Output directory for compliance data
└── README.md                   # Project documentation
```
## Prerequisites

To execute this framework, the Control Node must have the following installed:
- Python 3.x
- Ansible (core)
- OpenSSH Client

The Target Node requires:
- Ubuntu/Debian OS
- OpenSSH Server running
- A user with `sudo` privileges configured for SSH key-based authentication.

## Execution Guide

### 1. Configuration Enforcement (Ansible)

To apply the security baseline to the target servers defined in the inventory file, run the main playbook. The `-K` flag ensures secure prompt for the privilege escalation (sudo) password.

` ` `bash
ansible-playbook -i hardening/inventory/hosts.ini hardening/playbooks/hardening.yml -K
` ` `

*Note: The Ansible roles are built to be idempotent. Subsequent runs will only report changes if a configuration drift is detected.*

### 2. Compliance Auditing (Python)

Once the hardening process is complete, execute the scanner to validate the system's compliance state.

` ` `bash
python3 scanner/main.py
` ` `

### 3. Output and Reporting

The scanner will generate a standardized JSON report detailing the pass/fail state of each evaluated security control. The output is saved locally at `scanner/report/report.json`.

**Example Output:**

` ` `json
{
    "ssh_root_login_disabled": "PASS",
    "ssh_empty_passwords_disabled": "PASS",
    "firewall_ufw_active": "PASS"
}
` ` `

## Future Roadmap

- [ ] Expansion of Ansible roles to include auditd configuration and logging policies.
- [ ] Integration of OpenSCAP for deeper, standard-compliant vulnerability scanning.
- [ ] Implementation of a CI/CD pipeline (e.g., GitHub Actions) to automatically spin up a container, run the hardening playbook, and execute the scanner on every push.
- [ ] Support for RHEL/CentOS-based distributions.

## Author

Developed as a proof-of-concept for automated enterprise Linux security and DevSecOps practices.
