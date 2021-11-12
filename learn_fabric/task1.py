from fabric import Connection

result = Connection("127.0.0.1").run("ls $HOME", hide=True)
msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
print(msg.format(result))
