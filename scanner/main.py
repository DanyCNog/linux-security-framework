import subprocess
import json

# Define o alvo
TARGET_IP = "172.16.89.131"
TARGET_USER = "fogadmin"

def check_security_rule(command_to_run, expected_output=None):
    """ Executa um comando via SSH e verifica o resultado. """
    command = f"ssh {TARGET_USER}@{TARGET_IP} \"{command_to_run}\""
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Se exigirmos um output específico (ex: "active")
        if expected_output:
            if result.returncode == 0 and expected_output in result.stdout:
                return "PASS"
            return "FAIL"
        # Se apenas quisermos saber se o comando correu bem (ex: grep encontrou a linha)
        else:
            if result.returncode == 0:
                return "PASS"
            return "FAIL"
    except Exception as e:
        return f"ERROR: {str(e)}"

def main():
    print("🔍 A iniciar o Compliance Scanner (CIS Benchmarks)...\n")
    report = {}
    
    # 1. SSH Hardening Checks
    print("⏳ A verificar: PermitRootLogin...")
    report["ssh_root_login_disabled"] = check_security_rule("grep '^PermitRootLogin no' /etc/ssh/sshd_config")
    
    print("⏳ A verificar: PermitEmptyPasswords...")
    report["ssh_empty_passwords_disabled"] = check_security_rule("grep '^PermitEmptyPasswords no' /etc/ssh/sshd_config")
    
    # 2. Firewall Checks (NOVO)
    print("⏳ A verificar: Estado da Firewall (UFW)...")
    # O systemctl is-active verifica o status do serviço sem precisar de sudo
    report["firewall_ufw_active"] = check_security_rule("systemctl is-active ufw", expected_output="active")

    # Mostra o resultado final
    print("\n📊 Relatório de Compliance:")
    print(json.dumps(report, indent=4))
    
    # Guarda o relatório
    report_path = "scanner/report/report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=4)
        
    print(f"\n✅ Relatório guardado com sucesso em: {report_path}")

if __name__ == "__main__":
    main()
