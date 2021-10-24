# B2C2 Client

This project contains a command line app called `b2c2` that allows you perform trading
operations through B2C2 liquidity provider.

## Setting Credentials

In order the app to work, you need to provide credentials through environment variables.
You can set variables on the console, prior to running the app:
```
export TOKEN=abcdefghiklmnopqrstuvwxyz
```

Alternatively, you can create a file named `.env` and place variables within this file:
```
TOKEN=abcdefghiklmnopqrstuvwxyz
```

## End User Installation
### Building the wheel file

```bash
$ python -m venv venv
$ source venv/bin/activate
(venv) $ pip install build
(venv) $ python -m build
```

### Installing the app through wheels

```bash
$ pip install b2c2_client-0.0.1-py3-none-any.whl
$ b2c2
```

## Developer Installation

### Running the app without installation

```bash
$ python -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ python -m b2c2.cli.main
```

### Testing against the Mock Server

```bash
(venv) $ pip install -r b2c2/mockserver/requirements.txt
(venv) $ uvicorn b2c2.mockserver.main:app
```

On another console, you may run the app with local settings:

```bash
$ source venv/bin/activate
(venv) $ export LOCAL=1  # to indicate using local server on 127.0.0.1:8000
(venv) $ export TOKEN=abcdefghiklmnopqrstuvwxyz
(venv) $ python -m b2c2.cli.main
```
