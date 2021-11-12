# learn_fabric
The purpose of this repo is to learn package [fabric]()

# Virtual Environment
We use [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)

```shell
mkvirtualenv --system-site-packages --python=python3 learn_fabric
pip install -r requirements.txt
```

# Workflow

Using localhost ("127.0.0.1") as the remote worker

## Generating private/public keys
### Current  
Manually created with `ssh-keygen`
### Target  
Automatic creation (with _fabric_ or _paramiko_ ?)

## Deploying public key on remote host
### Current 
Deployed with _paramiko_; requires login with password
### Target  
- Capture the login and password when user logins to the web reflectivity application. Assumed these credentials are the same as those required to login in the remote worker.
- Deploy with _fabric_ instead of _paramiko_ (however, _fabric_ uses _paramiko_ under the hood)

## Remote execution
### Current 
Running a shell command remotely with _fabric_, for instance `Connection("127.0.0.1").run("ls $HOME")`

## Cleanup
### Current 
Not implemented
### Target  
- remove the public key from file _authorized_keys_ in the remote worker
- remove the private/public key files from the web_reflectivity host