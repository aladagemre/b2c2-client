# -*- coding: utf-8 -*-
import logging
import uuid
from typing import List

import requests

from b2c2.api_client.errors import get_api_error_by_code
from b2c2.api_client.exceptions import (
    HTTPException,
    NotFound,
    get_http_exception_by_code,
)
from b2c2.common.models import (
    Balance,
    FillOrKillOrderRequest,
    Instrument,
    MarketOrderRequest,
    OrderResponse,
    RFQResponse,
    Trade,
)

logger = logging.getLogger(__name__)


class B2C2Client:
    API_URL = "https://api.uat.b2c2.net"

    def __init__(self, token, api_url=None):
        self.token = token
        self.api_url = api_url or self.API_URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {self.token}",
        }

    def _raise_api_errors(self, response_json):
        if isinstance(response_json, list):
            # returned data, no problem.
            return
        errors = response_json.get("errors")
        if not errors:
            return

        api_errors = []
        for error in errors:
            code = error.get("code")
            message = error.get("message")
            error = get_api_error_by_code(code)(message)
            api_errors.append(error)
            # Log all the API errors sent.
            logger.error(error)

        # Raise the first error
        raise api_errors[0]

    def _make_request(self, url: str, method="get", data: dict = None):
        """
        requests.get/post wrapper handling exceptions
        :param url: URL to make request to
        :param method: "get" or "post"
        :param data: data to post
        :return: response in json format
        """
        try:
            if method == "get":
                response = requests.get(url, headers=self.headers)
            elif method == "post":
                response = requests.post(url, json=data, headers=self.headers)
            else:
                logger.warning("Invalid request type:", method)
                return

            self._raise_api_errors(response.json())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as exc:
            exception_class = get_http_exception_by_code(response.status_code)
            if exception_class:
                raise exception_class()
            else:
                raise HTTPException(exc=exc)
        except requests.exceptions.ConnectionError as _:
            logger.exception("Error Connecting Server")
        except requests.exceptions.Timeout as _:
            logger.exception("Timeout Error")
        except requests.exceptions.RequestException as _:
            logger.exception("Unknown error")

    def _get(self, endpoint: str):
        """
        Performs get request to the given endpoint.
        :param endpoint: Ex: /balance/
        :return: Response in json format
        """
        return self._make_request(f"{self.api_url}{endpoint}", method="get")

    def _post(self, endpoint: str, data: dict):
        """
        Performs POST request to the given endpoint
        :param endpoint: Ex: /order/
        :param data: Data dictionary
        :return:
        """
        return self._make_request(f"{self.api_url}{endpoint}", method="post", data=data)

    def get_balance(self):
        """
        Returns the account balance
        :return: `Balance` object containing quantities for each asset (USD, BTC, etc.)
        """
        balance_dict = self._get("/balance/")
        return Balance(**balance_dict)

    def list_instruments(self):
        """
        Returns the instruments available for trading.
        :return: A list of Instrument objects (with name attribute).
        """
        try:
            instruments = self._get("/instruments/")
            return [Instrument(**instrument) for instrument in instruments]
        except ConnectionError as exc:
            logger.exception("Could not connect to the server. Please try again later.")
        except:
            logger.exception("Could not perform the request. Please try again later.")

    def get_rfq(self, instrument, side, quantity):
        """
        Sends a `RFQ (request for quote)` and returns the response from the server
        :param instrument: Instrument object or instrument name (Ex: "BTCUSD.SPOT")
        :param side: "buy" or "sell"
        :param quantity: A numerical value to be handled as Decimal.
        :return: `RFQResponse` object
        """
        if isinstance(instrument, Instrument):
            instrument = instrument.name
        data = dict(
            instrument=instrument,
            side=side,
            quantity=str(quantity),
            client_rfq_id=str(uuid.uuid4()),
        )
        response = self._post("/request_for_quote/", data=data)
        if not response:
            logger.error("Could not get RFQ", extra=dict(data=data))
            return None
        return RFQResponse(**response)

    def create_fok_order(self, fok_order_request: FillOrKillOrderRequest):
        return self.create_order(fok_order_request.dict())

    def create_mkt_order(self, mkt_order_request: MarketOrderRequest):
        return self.create_order(mkt_order_request.dict())

    def create_order(self, order_data):
        response = self._post("/order/", data=order_data)
        if not response:
            raise Exception("Got invalid response from order endpoint.")

        order_response = OrderResponse(**response)

        if order_response.is_rejected:
            logger.exception(
                "Order %s was rejected",
                order_response.order_id,
                extra={
                    "order_request": order_data,
                    "order_response": order_response,
                },
            )
        else:
            logger.info(
                "Order %s was successfully placed",
                order_response.order_id,
                extra={
                    "order_request": order_data,
                    "order_response": order_response,
                },
            )
        return order_response

    def get_order_history(self) -> List[OrderResponse]:
        """
        Returns the list of orders performed.
        :return: List[OrderResponse]
        """
        order_list = self._get("/order/")
        return [OrderResponse(**order) for order in order_list]

    def get_order_detail(self, order_id) -> OrderResponse:
        """
        Returns details of a particular order
        :param order_id: the ID of the order
        :return: OrderResponse object
        """
        try:
            order = self._get(f"/order/{order_id}/")
            return OrderResponse(**order)
        except NotFound:
            logger.exception("Order not found: {}".format(order_id))
        return None

    def get_trade_history(self) -> List[Trade]:
        """
        Returns the list of trade objects performed.
        :return: List[Trade] objects
        """
        trade_list = self._get("/trade/")
        return [Trade(**trade) for trade in trade_list]

    def get_trade_detail(self, trade_id) -> Trade:
        """
        Returns details of a particular trade
        :param trade_id: the ID of the trade
        :return: Trade object
        """
        try:
            trade = self._get(f"/trade/{trade_id}")
            return Trade(**trade)
        except NotFound:
            logger.exception("Trade not found: {}".format(trade_id))
        return None

    def check_connection(self):
        """Checks whether we can connect to the server or not."""
        try:
            requests.get(f"{self.api_url}/instruments/", headers=self.headers)
            return True
        except (ConnectionError, requests.exceptions.ConnectionError) as exc:
            logger.exception("Connection could not be established with the server.")
            return False
