# -*- coding: utf-8 -*-
import datetime
import logging
import time
from decimal import Decimal

from PyInquirer import prompt
from rich.console import Console
from rich.table import Table

import b2c2.cli.questions as q
from b2c2.api_client.api import B2C2Client
from b2c2.cli.config import ConfigManager
from b2c2.cli.decorators import check_connection_before
from b2c2.cli.utils import (
    print_green,
    print_red,
    prompt_decimal,
    prompt_integer,
    prompt_list,
    prompt_string,
    prompt_yes_no,
)
from b2c2.common.models import (
    FillOrKillOrderRequest,
    Instrument,
    MarketOrderRequest,
    Side,
)
from b2c2.common.settings import API_URL


class CommandLineInterface:
    def __init__(self, config: ConfigManager):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.token = self.config.get_token()
        self.api_url = self.config.get_api_url()
        self.api_client = None

        if not self.token:
            # If no token provided, ask for one.
            self.token_settings()

        self.create_client()

        self.action_map = {
            "List Instruments": self.list_instruments,
            "Request for Quote (RFQRequest)": self.request_for_quote,
            "Create Order": self.create_order,
            "Display Balance": self.display_balance,
            "Display Order History": self.display_order_history,
            "Display Trade History": self.display_trade_history,
            "Display Order Details": self.display_order_details,
            "Display Trade Details": self.display_trade_details,
            "Token Settings": self.token_settings,
            "API URL Settings": self.api_url_settings,
            "Check connection": self.check_api_connection,
            "Quit": quit,
        }

    def create_client(self) -> None:
        """
        Creates and sets a new client with provided credentials.
        """
        self.api_client = B2C2Client(token=self.token, api_url=self.api_url)

    def execute_command(self, action) -> None:
        """
        Generic method for executing a menu action.
        :param action: the title of the menu item
        """
        self.action_map[action]()

    @check_connection_before
    def list_instruments(self) -> None:
        """
        Lists the instruments available. Upon chosing one, asks for RFQ permission.
        """
        instruments = self.api_client.list_instruments()
        if not instruments:
            self.logger.error(
                "Could not connect to the server. Please try again later."
            )
            return
        question = q.get_list_instruments_question(
            [instrument.name for instrument in instruments]
        )
        answer = prompt(question).get("instrument_action")
        if answer == "No Thanks":
            return
        self.request_for_quote(instrument_name=answer)

    @check_connection_before
    def request_for_quote(self, instrument_name=None) -> None:
        """
        Creates a request for quote (RFQ) and asks for execution permission.
        If given, creates a FOK or MKT order and displays the result of the order,
        together with the balance information
        :param instrument_name: the name of the instrument. Ex: BTCUSD.SPOT
        """
        if not instrument_name:
            instrument_name = prompt_string("Instrument:")
        side = prompt_list("Side:", ["buy", "sell"])
        quantity = prompt_decimal("Quantity")

        # Make RFQ Request
        rfq_response = self.api_client.get_rfq(instrument_name, side, quantity)
        if not rfq_response:
            print_red(
                "Could not get response from the server. Please check your connection."
            )
            return

        rfq_response.display()

        # Ask for execution permission
        execute_order = prompt_yes_no(
            "Do you want to execute an order with these details?"
        )
        if execute_order:
            order_type = prompt_list("Order Type:", ["FOK", "MKT"])
            instrument = Instrument(name=rfq_response.instrument)
            if instrument.type == "CFD":
                force_open = prompt_yes_no(
                    "Do you want to open a new contract instead of closing existing ones?"
                )
            else:
                force_open = False

            executing_unit = prompt_string("Executing Unit:")
            validity_seconds = prompt_integer("Validity in seconds:", default=10)
            valid_until = datetime.datetime.utcfromtimestamp(
                time.time() + validity_seconds
            ).strftime("%Y-%m-%dT%H:%M:%S")

            if order_type == "FOK":
                slippage = prompt_decimal(
                    "Accepted Slippage in Basis Points:",
                    default=Decimal(2.00),
                    boundaries=(Decimal(0.0), Decimal(20.0)),
                )
                price = prompt_decimal("Price:", default=rfq_response.price)
                fok_order_request = FillOrKillOrderRequest(
                    instrument=instrument.name,
                    side=side,
                    quantity=quantity,
                    valid_until=valid_until,
                    executing_unit=executing_unit,
                    force_open=force_open,
                    price=price,
                    acceptable_slippage_in_basis_points=slippage,
                )
                order_response = self.api_client.create_fok_order(
                    fok_order_request=fok_order_request
                )

            elif order_type == "MKT":
                mkt_order_request = MarketOrderRequest(
                    instrument=instrument.name,
                    side=side,
                    quantity=quantity,
                    valid_until=valid_until,
                    executing_unit=executing_unit,
                    force_open=force_open,
                )
                order_response = self.api_client.create_mkt_order(mkt_order_request)

            """
            order_response = self.api_client.create_order_from_rfq(
                rfq=rfq_response,
                order_type=order_type,
                valid_until=valid_until,
                executing_unit=executing_unit,

            )
            """
            if order_response.is_rejected:
                print_red("\nYour order was rejected.\n")
            else:
                print_green(f"\nYour order was successfully placed.\n")

            order_response.display()
            self.display_balance()

    @check_connection_before
    def create_order(self) -> None:
        """
        Menu for creating an order.
        """
        self.list_instruments()

    @check_connection_before
    def display_balance(self) -> None:
        """
        Menu for displaying balance
        """
        balance = self.api_client.get_balance()
        balance.display()

    @check_connection_before
    def display_order_history(self) -> None:
        """
        Menu for displaying order history
        """
        orders = self.api_client.get_order_history()
        if not orders:
            print_red("No orders yet.")
            return

        columns = [
            "created",
            "order_id",
            "client_order_id",
            "quantity",
            "side",
            "instrument",
            "price",
            "executed_price",
            "executing_unit",
        ]
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        for column in columns:
            table.add_column(column)
        for order in orders:
            data = [str(order.__dict__.get(col)) for col in columns]
            if order.executed_price is None:
                style = "grey37"
            elif order.side == Side.buy:
                style = "green"
            elif order.side == Side.sell:
                style = "red"
            table.add_row(*data, style=style)
        console.print(table)

    @check_connection_before
    def display_trade_history(self) -> None:
        """
        Menu for displaying trade history
        """
        trades = self.api_client.get_trade_history()
        if not trades:
            print_red("No trades yet.")
            return

        columns = [
            "created",
            "order",
            "trade_id",
            "quantity",
            "side",
            "instrument",
            "price",
            "executing_unit",
            "origin",
            "rfq_id",
        ]
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        for column in columns:
            table.add_column(column)
        for trade in trades:
            data = [str(trade.__dict__.get(col)) for col in columns]
            if trade.side == Side.buy:
                style = "green"
            elif trade.side == Side.sell:
                style = "red"
            else:
                style = "white"
            table.add_row(*data, style=style)
        console.print(table)

    @check_connection_before
    def display_order_details(self) -> None:
        """
        Menu for displaying a particular order's details
        """
        order_id = prompt_string("Enter order_id / client_order_id:")
        order = self.api_client.get_order_detail(order_id)
        if order:
            order.display()

    @check_connection_before
    def display_trade_details(self) -> None:
        """
        Menu for displaying a particular trade's details
        """
        trade_id = prompt_string("Enter trade_id:")
        trade = self.api_client.get_trade_detail(trade_id)
        if trade:
            trade.display()

    def _set_api_url(self) -> None:
        api_url = prompt_string("Please provide API URL:", default=API_URL)
        if api_url:
            self.api_url = api_url
            self.config.set_api_url(api_url)
            self.config.save_config()
            self.logger.info("API URL has been set.")
            self.create_client()
            self.logger.info("B2C2 Client has bee created.")
        elif api_url == dict():
            quit()

    def _set_token(self) -> None:
        """
        Asks for new token, sets it and creates a client with the token.
        """
        token = prompt_string("Please provide your token:")
        if token:
            self.token = token
            self.config.set_token(token)
            self.config.save_config()
            self.logger.info("Your token has been saved.")
            self.create_client()
            self.logger.info("B2C2 client has been created.")
        elif token == dict():
            quit()

    def token_settings(self) -> None:
        """
        Menu for token settings
        """
        if self.token:
            print(f"Your token is set as: {self.token}")
            if prompt_yes_no("Do you want to reset it?"):
                print("Your token has been reset.")
                self._set_token()

        while not self.token:
            self._set_token()

    def api_url_settings(self) -> None:
        """
        Menu for API URL settings
        """
        if self.api_url:
            print(f"API URL is set as: {self.api_url}")
            if prompt_yes_no("Do you want to reset it?"):
                print("API URL has been reset.")
                self._set_api_url()

    def check_api_connection(self):
        return self.api_client.check_connection()
