import subprocess
import json

# Target node configuration
TARGET_IP = "172.16.89.131"
TARGET_USER = "fogadmin"

def check_security_rule(command_to_run, expected_output=None):
    """
    Executes a shell command via SSH on the target node and validates the output.
    Returns 'PASS' if the rule is compliant, otherwise 'FAIL'.
    """
    command = f"ssh {TARGET_USER}@{TARGET_IP} \"{command_to_run}\""
    
    try:
        # Execute the remote command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Evaluate based on specific expected output (e.g., service status)
        if expected_output:
            if result.returncode == 0 and expected_output in result.stdout:
                return "PASS"
            return "FAIL"
        # Evaluate based solely on command exit code (e.g., grep matches)
        else:
            if result.returncode == 0:
                return "PASS"
            return "FAIL"
    except Exception as e:
        return f"ERROR: {str(e)}"

def main():
    print("Starting the Compliance Scanner (CIS Benchmarks)...\n")
    report = {}
    
    # 1. SSH Hardening Checks
    print("Checking rule: PermitRootLogin...")
    report["ssh_root_login_disabled"] = check_security_rule("grep '^PermitRootLogin no' /etc/ssh/sshd_config")
    
    print("Checking rule: PermitEmptyPasswords...")
    report["ssh_empty_passwords_disabled"] = check_security_rule("grep '^PermitEmptyPasswords no' /etc/ssh/sshd_config")
    
    # 2. Firewall Checks
    print("Checking rule: UFW Status...")
    report["firewall_ufw_active"] = check_security_rule("systemctl is-active ufw", expected_output="active")

    # Display the final compliance report
    print("\nCompliance Report:")
    print(json.dumps(report, indent=4))
    
    # Export the report to a JSON file
    report_path = "scanner/report/report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=4)
        
    print(f"\nReport successfully saved to: {report_path}")

if __name__ == "__main__":
    main()
