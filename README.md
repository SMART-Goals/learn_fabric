# learn_fabric
The purpose of this repo is to learn package [fabric]()

# Setup for Development with a Virtual Environment
We use [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)

```shell
mkvirtualenv --system-site-packages --python=python3 learn_fabric
pip install -r requirements.txt
```

# Run the Workflow

Using localhost ("127.0.0.1") as the remote worker:
- run a command remotely
- transfer a script, then run it. The script creates a file in the remote worker

```
python workflow.py
```

# Current Status
## Generating temporary private/public key files
### Current  
Automatic creation with `ssh-keygen`
### Target  
Automatic creation with _fabric_ (or _paramiko_ ?)

## Deploying public key on remote host
### Current 
Deployed with _paramiko_; requires one time login credentials to the remote worker
### Target  
- Capture the login and password when user logins to the web reflectivity application. Assumed these credentials are the same as those required to login in the remote worker.
- Deploy with _fabric_ instead of _paramiko_ (however, _fabric_ uses _paramiko_ under the hood)

## Remote execution
### Current 
Running a shell command remotely with _fabric_, for instance `Connection("127.0.0.1").run("ls $HOME")`
Transfer file to the remote worker with _fabric_, for instance `Connection("127.0.0.1").run("ls $HOME")`

## Cleanup
### Current 
- Context manager removes the temporary SSH key from the _authorized_keys_ file in the remote worker
- Context manager removes the temporary private/public SSH key files from the host
