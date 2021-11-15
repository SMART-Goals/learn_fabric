# package imports
from learn_fabric.create_key import generate_public_key_file
from learn_fabric.sshclient import create_ssh_client

# third party imports
import fabric

# standard imports
from contextlib import contextmanager
import os
from typing import Optional


def run_command_remotely(command: str,
                         user_name: str,
                         worker_address: str,
                         public_key_file: Optional[str] = None):
    r"""
    Run a command on a remote worker.
    :param command: shell command to run
    :param user_name: username that will run remotely
    :param worker_address: IP address or name of the remote worker
    :param public_key_file: if ``None``, a private/public key will be created for running this command and the
    public key will be appended to the authorized_keys file in the remote worker. A login will be required for this
    step. If not ``None``, it is assume that all the previous steps have already happened.
    :return paramiko.invoke.runners.Result:
    """
    if public_key_file:  # persistent private/public key, also assumed public key in
        tunnel = fabric.Connection(host=worker_address,
                                   user=user_name,
                                   connect_kwargs={"key_filename": public_key_file}
                                   )
        result = tunnel.run(command)
    else:
        with generate_public_key_file() as key_file:
            with create_ssh_client(key_file, worker_address) as _:
                tunnel = fabric.Connection(host=worker_address,
                                           user=user_name,
                                           connect_kwargs={"key_filename": key_file})
                result = tunnel.run(command)
            # exiting context: remove the public key from the host's authorized_keys file
        # exiting context: remove the private and public SSH key files
    return result


@contextmanager
def fabric_tunnel(user_name: str,
                  worker_address: str,
                  public_key_file: Optional[str] = None):
    r"""
    Run a command on a remote worker.
    :param command: shell command to run
    :param user_name: username that will run remotely
    :param worker_address: IP address or name of the remote worker
    :param public_key_file: if ``None``, a private/public key will be created for running this command and the
    public key will be appended to the authorized_keys file in the remote worker. A login will be required for this
    step. If not ``None``, it is assume that all the previous steps have already happened.
    :return paramiko.invoke.runners.Result:
    """
    try:
        if public_key_file:  # persistent private/public key, also assumed public key in
            yield fabric.Connection(host=worker_address,
                                    user=user_name,
                                    connect_kwargs={"key_filename": public_key_file})
        else:
            with generate_public_key_file() as key_file:
                with create_ssh_client(key_file, worker_address) as _:
                    yield fabric.Connection(host=worker_address,
                                            user=user_name,
                                            connect_kwargs={"key_filename": key_file})
                # exiting context: remove the public key from the host's authorized_keys file
            # exiting context: remove the private and public SSH key files
    finally:
        pass


if __name__ == '__main__':
    remote_worker = "127.0.0.1"  # "remote" worker
    user_name = "jbq"

    with fabric_tunnel(user_name, remote_worker) as tunnel:

        print(r"""
        #
        # run command `ls $HOME` remotely
        #
        """)
        command = "ls $HOME"  # job to be run in the "remote" worker
        result = tunnel.run(command)
        print(result.stdout)

        print(r"""
        #
        # run a script remotely. Script creates an output file containing the line "Hello World!"
        #
        """)
        # create the script script
        out_file = "/tmp/output.txt"
        script = r"""out_file = "{0}"
contents = "Hello World!\n"
open("{0}", "w").write(contents)
""".format(out_file)
        script_file, script_file_name = "/tmp/script.py", "script.py"
        open(script_file, "w").write(script)
        # transfer the script to the remote worker
        tunnel.put(script_file)  # transfer the script to the user's home directory
        # make sure the output file resulting from running the script doesn't exist
        if os.path.exists(out_file):
            os.remove(out_file)
        tunnel.run(f"python $HOME/{script_file_name}")  # execute the script remotely
        # verify the output file was created
        print("File created. Its contents are:")
        print(open(out_file).read())
