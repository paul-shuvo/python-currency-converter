# -*- coding: future_fstrings -*-

import requests
from bs4 import BeautifulSoup
import json
import re
import itertools


class CurrencyConverter:
    def __init__(self, from_=None, to=None, map_currency: bool = False) -> None:
        self.from_ = from_ if isinstance(from_, list) else [from_]
        self.to = to if isinstance(to, list) else [to]
        self.map_currency = map_currency
        self.currency_codes = [
            "AFN",
            "ALL",
            "DZD",
            "AOA",
            "ARS",
            "AMD",
            "AWG",
            "AUD",
            "AZN",
            "BSD",
            "BHD",
            "BBD",
            "BDT",
            "BYR",
            "BZD",
            "BMD",
            "BTN",
            "XBT",
            "BOB",
            "BAM",
            "BWP",
            "BRL",
            "BND",
            "BGN",
            "BIF",
            "XPF",
            "KHR",
            "CAD",
            "CVE",
            "KYD",
            "FCFA",
            "CLP",
            "CLF",
            "CNY",
            "CNY",
            "COP",
            "CF",
            "CDF",
            "CRC",
            "HRK",
            "CUC",
            "CZK",
            "DKK",
            "DJF",
            "DOP",
            "XCD",
            "EGP",
            "ETB",
            "FJD",
            "GMD",
            "GBP",
            "GEL",
            "GHS",
            "GTQ",
            "GNF",
            "GYD",
            "HTG",
            "HNL",
            "HKD",
            "HUF",
            "ISK",
            "INR",
            "IDR",
            "IRR",
            "IQD",
            "ILS",
            "JMD",
            "JPY",
            "JOD",
            "KZT",
            "KES",
            "KWD",
            "KGS",
            "LAK",
            "LBP",
            "LSL",
            "LRD",
            "LYD",
            "MOP",
            "MKD",
            "MGA",
            "MWK",
            "MYR",
            "MVR",
            "MRO",
            "MUR",
            "MXN",
            "MDL",
            "MAD",
            "MZN",
            "MMK",
            "NAD",
            "NPR",
            "ANG",
            "NZD",
            "NIO",
            "NGN",
            "NOK",
            "OMR",
            "PKR",
            "PAB",
            "PGK",
            "PYG ",
            "PHP",
            "PLN",
            "QAR",
            "RON",
            "RUB",
            "RWF",
            "SVC",
            "SAR",
            "RSD",
            "SCR",
            "SLL",
            "SGD",
            "SBD",
            "SOS",
            "ZAR",
            "KRW",
            "VES",
            "LKR",
            "SDG",
            "SRD",
            "SZL",
            "SEK",
            "CHF",
            "TJS",
            "TZS",
            "THB",
            "TOP",
            "TTD",
            "TND",
            "TRY",
            "TMT",
            "UGX",
            "UAH",
            "AED",
            "USD",
            "UYU",
            "UZS",
            "VND",
            "XOF",
            "YER",
            "ZMW",
            "ETH",
            "EUR",
            "LTC",
            "TWD",
            "PEN",
        ]

    def available_currencies(self):
        return self.currency_codes

    def from_currency(self, from_):
        self.from_ = from_ if isinstance(from_, list) else [from_]
        return self

    def to_currency(self, to):
        self.to = to if isinstance(to, list) else [to]
        return self

    def get_rates(self, is_json=False):
        if self.map_currency and len(self.from_) != len(self.to):
            raise ValueError(
                f"if you are mapping currency index-wise, the length of from should be equal to the length of to"
            )

        conversions = {}

        currency_maps = (
            zip(self.from_, self.to)
            if self.map_currency
            else list(itertools.product(self.from_, self.to))
        )
        for i, currency_map in enumerate(currency_maps):
            from_cur, to_cur = currency_map
            from_cur = from_cur.upper()
            to_cur = to_cur.upper()

            if from_cur not in self.currency_codes:
                raise ValueError(
                    f"{from_cur} is either not a valid currency code or not supported"
                )

            if to_cur not in self.currency_codes:
                raise ValueError(
                    f"{to_cur} is either not a valid currency code or not supported"
                )

            conversion = {"from": from_cur, "to": to_cur}
            conversion["rate"] = self.fetch_rate(from_cur=from_cur, to_cur=to_cur)

            conversions[i] = conversion

        return conversions if not is_json else json.dumps(conversions, indent=4)

    def fetch_rate(self, from_cur: str, to_cur: str):
        response = requests.get(
            f"https://www.google.com/search?q={from_cur}+to+{to_cur}"
        )

        if response.status_code != 200:
            return "No response from the server"
        else:
            soup = BeautifulSoup(response.content, "lxml")
            try:
                rate = soup.find_all("div", class_="BNeawe iBp4i AP7Wnd")[1].string.split(
                    " "
                )[0]
            except:
                print('Error occured in extracting the currency rate. Please submit a github issue.')
                
            if not re.compile(r"^[0-9]*$").match(re.sub(r"[\s|,|.]", "", rate)):
                return None
            else:
                rate = float(re.sub(r"[\s|,]", "", rate))
                return rate


# cc = (
#     CurrencyConverter(map_currency=True)
#     .from_currency(from_=["jpy", "gbp"])
#     .to_currency(to=["usd", "inr"])
# )
# # print(cc.convert())
# cc = CurrencyConverter()
# print(cc.fetch_rate('USD', 'JPY'))
