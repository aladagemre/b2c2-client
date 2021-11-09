# -*- coding: utf-8 -*-
import datetime
from decimal import Decimal
from http import HTTPStatus

from pytest_mock import MockerFixture

from b2c2.api_client.api import B2C2Client
from b2c2.common.models import FillOrKillOrderRequest, Instrument


def test_get_balance(mocker: MockerFixture, client: B2C2Client, balance: dict):
    """Given a balance response, test whether client can retrieve properly"""
    fake_resp = mocker.Mock()
    fake_resp.json = mocker.Mock(return_value=balance)
    fake_resp.status_code = HTTPStatus.OK
    mocker.patch("requests.get", return_value=fake_resp)

    balance_response = client.get_balance()
    assert balance_response["USD"] == balance["USD"]


def test_get_instruments(mocker: MockerFixture, client: B2C2Client, instruments: dict):
    """Given an /instrument/ response, test whether client can retrieve properly"""
    fake_resp = mocker.Mock()
    fake_resp.json = mocker.Mock(return_value=instruments)
    fake_resp.status_code = HTTPStatus.OK
    mocker.patch("requests.get", return_value=fake_resp)

    instruments_response = client.list_instruments()
    assert Instrument(name="BTCUSD.SPOT") in instruments_response


def test_order(mocker: MockerFixture, client: B2C2Client, order: dict):
    """Given an POST /order/ response, test whether client can process properly"""
    fake_resp = mocker.Mock()
    fake_resp.json = mocker.Mock(return_value=order)
    fake_resp.status_code = HTTPStatus.CREATED
    mocker.patch("requests.post", return_value=fake_resp)

    fok_order_request = FillOrKillOrderRequest(
        instrument="BTCUSD.SPOT",
        side="buy",
        quantity=Decimal("1.0"),
        valid_until=datetime.datetime.now() + datetime.timedelta(seconds=10),
        executing_unit="tag",
        force_open=False,
        price=Decimal("57635.3"),
        acceptable_slippage_in_basis_points=Decimal("2"),
    )
    order_response = client.create_fok_order(fok_order_request=fok_order_request)
    assert order_response.side == fok_order_request.side
    assert order_response.price == fok_order_request.price
    assert order_response.instrument == fok_order_request.instrument


def test_order_details(mocker: MockerFixture, client: B2C2Client, order_details: dict):
    """Given an GET /order/:orderID response, test whether client can retrieve properly"""
    fake_resp = mocker.Mock()
    fake_resp.json = mocker.Mock(return_value=order_details)
    fake_resp.status_code = HTTPStatus.OK
    mocker.patch("requests.get", return_value=fake_resp)
    order_response = client.get_order_detail(order_details["order_id"])
    assert order_response.instrument == order_details["instrument"]
    assert order_response.side == order_details["side"]
    assert order_response.price == Decimal(order_details["price"])


def test_order_history(mocker: MockerFixture, client: B2C2Client, order_history: dict):
    """Given an GET /order/ response, test whether client can retrieve properly"""
    fake_resp = mocker.Mock()
    fake_resp.json = mocker.Mock(return_value=order_history)
    fake_resp.status_code = HTTPStatus.OK
    mocker.patch("requests.get", return_value=fake_resp)
    order_response_list = client.get_order_history()
    assert len(order_response_list) == 1
    order_response = order_response_list[0]
    order_details = order_history[0]
    assert order_response.instrument == order_details["instrument"]
    assert order_response.side == order_details["side"]
    assert order_response.price == Decimal(order_details["price"])


def test_request_for_quote(
    mocker: MockerFixture, client: B2C2Client, request_for_quote: dict
):
    """Given an POST /request_for_quote/ response, test whether client can process properly"""
    fake_resp = mocker.Mock()
    fake_resp.json = mocker.Mock(return_value=request_for_quote)
    fake_resp.status_code = HTTPStatus.CREATED
    mocker.patch("requests.post", return_value=fake_resp)

    rfq_response = client.get_rfq(
        instrument=request_for_quote["instrument"],
        side=request_for_quote["side"],
        quantity=Decimal(request_for_quote["quantity"]),
    )

    assert rfq_response.instrument == request_for_quote["instrument"]
    assert rfq_response.side == request_for_quote["side"]
    assert rfq_response.quantity == Decimal(request_for_quote["quantity"])
    assert rfq_response.price


def test_trade_details(mocker: MockerFixture, client: B2C2Client, trade_details: dict):
    """Given an GET /trade/:tradeID response, test whether client can retrieve properly"""
    fake_resp = mocker.Mock()
    fake_resp.json = mocker.Mock(return_value=trade_details)
    fake_resp.status_code = HTTPStatus.OK
    mocker.patch("requests.get", return_value=fake_resp)
    trade_response = client.get_trade_detail(trade_details["trade_id"])
    assert trade_response.instrument == trade_details["instrument"]
    assert trade_response.side == trade_details["side"]
    assert trade_response.price == Decimal(trade_details["price"])


def test_trade_history(mocker: MockerFixture, client: B2C2Client, trade_history: dict):
    """Given an GET /trade/ response, test whether client can retrieve properly"""
    fake_resp = mocker.Mock()
    fake_resp.json = mocker.Mock(return_value=trade_history)
    fake_resp.status_code = HTTPStatus.OK
    mocker.patch("requests.get", return_value=fake_resp)
    trade_response_list = client.get_trade_history()
    assert len(trade_response_list) == 1
    trade_response = trade_response_list[0]
    trade_details = trade_history[0]
    assert trade_response.instrument == trade_details["instrument"]
    assert trade_response.side == trade_details["side"]
    assert trade_response.price == Decimal(trade_details["price"])
