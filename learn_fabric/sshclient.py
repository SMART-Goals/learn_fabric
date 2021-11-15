# third-party imports
import paramiko

# standard imports
from contextlib import contextmanager
from getpass import getpass
import os


@contextmanager
def create_ssh_client(key_file: str, remote_worker: str):
    r"""
    Context manager to append a public key into the authorized_keys file in the remote worker.
    Upon exiting the context, the key is remove from the authorized_keys file in the remote worker.
    :param key_file: absolute path to the public key file
    :param remote_worker: IP address or internet address of the remote worker
    :yield: None
    """
    success = False
    try:
        key = open(os.path.expanduser(key_file)).read()
        username = os.getlogin()
        password = getpass()
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(remote_worker, username=username, password=password)
        client.exec_command('mkdir -p ~/.ssh/')
        client.exec_command('touch ~/.ssh/authorized_keys')
        client.exec_command('/bin/cp ~/.ssh/authorized_keys ~/.ssh/authorized_keys.bak')
        client.exec_command('echo "%s >> ~/.ssh/authorized_keys" .' % key)
        client.exec_command('chmod 644 ~/.ssh/authorized_keys')
        client.exec_command('chmod 700 ~/.ssh/')
        success = True
        yield client
    finally:
        if success:
            client.exec_command('/bin/mv ~/.ssh/authorized_keys.bak ~/.ssh/authorized_keys')
