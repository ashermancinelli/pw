### Password Manager

#### Server-side

There is an example service script in the project (`example-pw.service`) which can be enabled through systemd:
```shell
$ sudo cp ./example-pw.service /etc/systemd/system
$ sudo systemctl enable pw
```

Also make sure to open whatever port you use through your firewall program.

#### Client-side

```python
$ pip install -r requirements.txt
$
$ # I recommend adding these to bashrc
$ export PWHOST=<ip address of server>
$
$ # Make sure this private key matches that on the server
$ export PWSECRETFILE=/path/to/private/key
$ export PATH=$PATH:/path/to/repo
$ pw
<decryted private data>
```
