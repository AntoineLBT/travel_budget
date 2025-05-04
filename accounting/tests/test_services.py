from decimal import Decimal

from django.test import TestCase
from hamcrest import assert_that, instance_of, is_in

from ..services import CurrencyRatesGetter


class TestCurrencyRatesGetter(TestCase):

    def test_get_exchange_rate(self) -> None:

        response = CurrencyRatesGetter.get_exchange_rate("USD", "NZD")

        assert_that(response.json(), instance_of(dict))
        assert_that("rates", is_in(response.json().keys()))
        assert_that("NZD", is_in(response.json()["rates"].keys()))

    def test_convert_amount(self) -> None:

        response = CurrencyRatesGetter.convert_amount("EUR", "NZD", Decimal(10000))

        assert_that(response, instance_of(Decimal))
