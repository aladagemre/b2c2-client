# B2C2 Client

This project contains a command line app called `b2c2` that allows you perform trading
operations through B2C2 liquidity provider.

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

Then you should set your token in the "Token Settings" menu.

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
(venv) $ python -m b2c2.cli.main
```

Then you should set your token in the "Token Settings" menu. You can update the API_URL in the menu as well.

## Restrictions

The sandbox API documentation is not comprehensive. So I had to make some assumptions.

* User receives a RFQ. However when performing an order, there is no rfq argument. I assume server looks for the most recent relevant RFQ and executes the order accordingly.
* There is no explanation on how to handle CFD vs SPOT. The sample balance in the API documentation indicate no CFDs. So I assumed it's the same as SPOT. When a user buys BTCUSD.CFD, then their BTC balance will increase, their USD balance will decrease. Leverage: 1X.
* I assume `order/force_open` argument is only available for CFD instruments. That's why, I removed this argument for SPOT instrument orders.
* Precisions page was not detailed enough. Precisions for displaying the balances were not clear. So I assumed the cryptos have 8 precision whereas fiat currencies have 2 precision point.
* There is no mention of the format of your error messages and when they return. I made an assumption.
* When an order is rejected, you return an OrderResponse with executed_price=None, instead of returning "1011 - Not enough balance – Not enough balance.". So I check for the former. However if an API Exception is thrown, it is handled as displaying error message.
* It is not clear whether the /balance response has a fixed set of keys (currencies). Because of that, I moved away from Modeling Balance with static fields, instead used a dictionary.
