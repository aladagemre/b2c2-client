# -*- coding: utf-8 -*-
import json

import pytest

from b2c2.api_client.api import B2C2Client


@pytest.fixture()
def client():
    return B2C2Client(token="token")


@pytest.fixture()
def balance():
    """Fixture that returns GET `/balance/` response."""
    with open("tests/resources/api/balance.json") as f:
        return json.load(f)


@pytest.fixture()
def instruments():
    """Fixture that returns GET `/instruments/` response."""
    with open("tests/resources/api/instruments.json") as f:
        return json.load(f)


@pytest.fixture()
def order():
    """Fixture that returns POST `/order/` response."""
    with open("tests/resources/api/order.json") as f:
        return json.load(f)


@pytest.fixture()
def order_details():
    """Fixture that returns GET `/order/:orderId` response."""
    with open("tests/resources/api/order_details.json") as f:
        return json.load(f)


@pytest.fixture()
def order_history():
    """Fixture that returns GET `/order/` response."""
    with open("tests/resources/api/order_history.json") as f:
        return json.load(f)


@pytest.fixture()
def request_for_quote():
    """Fixture that returns POST `/request_for_quote/` response."""
    with open("tests/resources/api/request_for_quote.json") as f:
        return json.load(f)


@pytest.fixture()
def trade_details():
    """Fixture that returns GET `/trade/:tradeId` response."""
    with open("tests/resources/api/trade_details.json") as f:
        return json.load(f)


@pytest.fixture()
def trade_history():
    """Fixture that returns GET `/trade/` response."""
    with open("tests/resources/api/trade_history.json") as f:
        return json.load(f)
