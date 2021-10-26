# -*- coding: utf-8 -*-
from unittest import TestCase

from b2c2.common.models import Instrument


class TestInstrument(TestCase):
    def test_3_3(self):
        btcusd_spot = Instrument(name="BTCUSD.SPOT")
        self.assertEqual(btcusd_spot.type, "SPOT")
        self.assertEqual(btcusd_spot.base, "BTC")
        self.assertEqual(btcusd_spot.quote, "USD")

    def test_3_4(self):
        btcusd_spot = Instrument(name="BTCUSDT.SPOT")
        self.assertEqual(btcusd_spot.type, "SPOT")
        self.assertEqual(btcusd_spot.base, "BTC")
        self.assertEqual(btcusd_spot.quote, "USDT")

    def test_4_3(self):
        btcusd_spot = Instrument(name="USDTUSD.SPOT")
        self.assertEqual(btcusd_spot.type, "SPOT")
        self.assertEqual(btcusd_spot.base, "USDT")
        self.assertEqual(btcusd_spot.quote, "USD")
