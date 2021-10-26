# -*- coding: utf-8 -*-
from unittest import TestCase

import requests
import requests_mock

from b2c2.api_client import errors
from b2c2.api_client.api import B2C2Client


class TestAPIErrors(TestCase):
    def setUp(self) -> None:
        self.client = B2C2Client(token="abcdefg")

    def test_instrument_not_allowed(self):
        response = dict(
            errors=[
                {
                    "code": 1001,
                    "message": "Instrument not allowed – Instrument does not exist or you are not authorized to trade it.",
                }
            ]
        )
        with requests_mock.Mocker() as m:
            m.post(f"{self.client.api_url}/request_for_quote/", json=response)
            with self.assertRaises(errors.InstrumentNotAllowed) as context:
                self.client.get_rfq("NONEXISTENT", "buy", "1.0")
