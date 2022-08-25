import inspect
import sys
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


def SSHConnect(hostname, command):
    # result = ssh.connect(hostname, 22, username=username, password=GetCreds(username), auth_timeout=30, look_for_keys=True)
    ssh.connect(hostname, username="root", password="root", timeout=5)
    stdin, stdout, stderr = ssh.exec_command(command, timeout=3, get_pty=True)

    # stdin, stdout, stderr = ssh.exec_command('/sbin/ifconfig') -> simple exec ex.
    print(stdout.read().decode("utf-8"))


def main():
    SSHConnect("129.129.130.168", "cd /ioc/XCZU6EG-AD82 && ls -l")


if __name__ == "__main__":
    main()
