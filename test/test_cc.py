import pytest
from unittest.mock import Mock, patch
from currency_converter import CurrencyConverter


def test_init():
    cc = CurrencyConverter()
    assert isinstance(cc.from_, list)
    assert isinstance(cc.to, list)
    assert cc.from_[0] == None
    assert cc.to[0] == None


def test_available_currencies():
    cc = CurrencyConverter()
    assert isinstance(cc.available_currencies(), list)


def test_from_currency():
    cc = CurrencyConverter()
    assert cc.from_currency(["USD", "GBP"]).from_ == ["USD", "GBP"]


def test_to_currency():
    cc = CurrencyConverter()
    assert cc.to_currency(["USD", "GBP"]).to == ["USD", "GBP"]


def test_get_rates():
    with pytest.raises(ValueError):
        cc = CurrencyConverter("USD", "PKSD").get_rates()

    with pytest.raises(ValueError):
        cc = CurrencyConverter("MKTS", "USD").get_rates()

    with pytest.raises(AttributeError):
        cc = CurrencyConverter().get_rates()

    with pytest.raises(ValueError):
        cc = CurrencyConverter(map_currency=True)
        cc.from_currency("USD").to_currency(["GBP", "JPY"]).get_rates()

    cc = CurrencyConverter("USD", "JPY")
    assert isinstance(cc.get_rates(), dict)
    assert isinstance(cc.get_rates(True), str)

def test_fetch_rates():
     response_mock = Mock()
     response_mock.status_code = -1
     response_mock.json.return_value = {
          '12/25': 'Christmas',
          '7/4': 'Independence Day',
     }
     cc = CurrencyConverter(['JPY'], ['USD'])
     
     with patch('currency_converter.requests') as mock_requests:
          mock_requests.get.side_effect = response_mock
          assert cc.fetch_rate('JPY', 'USD') == "No response from the server"
     
         
     with patch('currency_converter.re.sub') as mock_sub:
          mock_sub.return_value = '10.93'
          assert cc.fetch_rate('GBP', 'USD') == None
          
          mock_sub.return_value = '1093'
          assert cc.fetch_rate('GBP', 'USD') == 1093

     with pytest.raises(Exception):
          cc.fetch_rate('Hello', 'World')
          
     
