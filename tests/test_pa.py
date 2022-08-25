import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


def MonitorProcess():
    ssh.connect("129.129.130.168", username="root", password="root", timeout=5)
    stdin, stdout, stderr = ssh.exec_command(
        "cd /ioc/XCZU6EG-AD82 && ls -l", timeout=3, get_pty=True
    )
    # stdin, stdout, stderr = ssh.exec_command('/sbin/ifconfig') -> simple exec ex.
    print(stdout.read().decode("utf-8"))


MonitorProcess()
