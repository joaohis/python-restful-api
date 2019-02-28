# Python RESTful API

Basic python RESTful API built with [web.py](http://webpy.org/) and SQL database with the login, logout and check-token functions.


## Dependencies

The project requires a SQL server and the following python modules:

* [web.py](http://webpy.org/);
* [MySQLdb interface](https://pypi.org/project/MySQL-python/);
* JSON encoder and decoder ([json](https://docs.python.org/2/library/json.html));
* Miscellaneous operating system interfaces ([os](https://docs.python.org/2/library/os.html));
* Secure hashes and message digests ([hashlib](https://docs.python.org/2/library/hashlib.html)).


## Configuration

Edit the following line at the `rest.py` file with your database information:
```python
db = web.database(dbn = 'mysql', db = 'python-restful-app', user = 'DB-USER', pw = 'DB-PASS')
```


## Usage

The server can be started locally by the command:
```bash
./rest.py
```

After insert the users and password at the database, you can test the login function with this [curl](https://curl.haxx.se/) command:
```bash
curl --header "Content-Type: application/json" --request POST --data '{"username": "USER", "password": "PASS"}' 127.0.0.1:8080/login
```
The API will return a token string if the user and password match with the database records.

Test if token is valid with this POST command:
```bash
curl --header "Content-Type: application/json" --request POST --data '{"token": "TOKEN"}' 127.0.0.1:8080/check-token
```

The token can be destroyed POSTing it at the logout function:
```bash
curl --header "Content-Type: application/json" --request POST --data '{"token": "TOKEN"}' 127.0.0.1:8080/check-logout
```