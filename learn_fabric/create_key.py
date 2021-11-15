# standard imports
from contextlib import contextmanager
from pathlib import Path
import random
from string import ascii_letters
import subprocess


@contextmanager
def generate_public_key_file() -> str:
    r"""
    Context manager creates a pair of private/public SSH key files and serves the path to the public key file
    Upon exiting the context, the private/public SSH key files are removed
    :return: public key file
    """
    suffix_length = 12
    file_name = f"id_rsa_{''.join(random.choice(ascii_letters) for _ in range(suffix_length))}"
    target_dir = Path.home() / ".ssh"
    private_file = target_dir / file_name
    public_file = target_dir / (file_name + ".pub")
    subprocess.run(['ssh-keygen', '-b', '2048', '-t', 'rsa', '-f', private_file, '-q', '-N', '""'])
    try:
        yield str(public_file)
    finally:
        private_file.unlink()
        public_file.unlink()
