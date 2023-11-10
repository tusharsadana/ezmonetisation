# stdlib
import re
from types import MappingProxyType
from typing import Callable, Union

# thirdparty
from dateutil.parser import parse


def is_object(string: str) -> Union[bool, str]:
    """
    Check that ent text longer than 8 chars - empirical value
    """
    string = string.strip()
    if len(string) > 8:
        return string
    return False


def is_fund_name(fund_name: str) -> Union[bool, str]:
    """
    Check fund name and rm L.P. postfix in case it is extracted
    """
    checked_fund_name = is_object(fund_name)
    if not checked_fund_name:
        return checked_fund_name
    counter = [1 for s in fund_name if s.isdigit()]
    if sum(counter) >= len(fund_name) // 2:
        return False
    first, last = checked_fund_name[:-5], checked_fund_name[-5:]
    # remove LP in the end of the fund name
    last = re.sub(r"\s*L\.*P\.*", "", last)
    # remove comma in the fund name
    checked_fund_name = re.sub(",", "", first + last)
    return checked_fund_name


def is_client_name(client_name: str) -> Union[bool, str]:
    """
    Check fund name and rm L.P. postfix in case it is extracted
    """
    checked_fund_name = is_object(client_name)
    if not checked_fund_name:
        return checked_fund_name
    counter = [1 for s in client_name if s.isdigit()]
    if sum(counter) >= len(client_name) // 2:
        return False
    return client_name


def convert_millions(amount_text: str) -> Union[str, bool]:
    if "mil" in amount_text:
        match = re.search(r"(\d{1,3})[,\.](\d{1,3})", amount_text)
        if match:
            millions = int(match.group(1)) * 1e6
            thousands = 0
            if len(match.group(2)) == 3:
                thousands = int(match.group(2)) * 1e3
            if len(match.group(2)) == 2:
                thousands = int(match.group(2)) * 1e4
            if len(match.group(2)) == 1:
                thousands = int(match.group(2)) * 1e5
            result = int(millions + thousands)
            return "{:0,.2f}".format(result)
    else:
        return False


def is_amount(string: str):
    """
    Check ent text if it contains amount - here it means
    text contains digits and ,.  (or it is dash - also possible)
    """
    try:
        amount = convert_millions(string)
    except Exception:
        amount = False
    if amount:
        return amount

    match = re.search(r"(\d{1,3}\s*[\.,]*\s*)+", string)
    if match:
        amount = match.group(0).strip()
        if not amount[-1].isdigit():
            amount = amount[:-1]
        amount = re.sub(r"[\s()]*", "", amount)
        if "," in amount:
            amount = amount.replace(",", "")
        return amount
    return False


def is_date(string, fuzzy=True) -> Union[bool, str]:
    """
    Return whether the string can be interpreted as a date.
    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        _ = parse(string, fuzzy=fuzzy)
        return string
    except ValueError:
        return False


def convert_date(string) -> Union[bool, str]:
    """
    Return whether the string can be interpreted as a date.
    :param string: str, string to check for date
    """
    try:
        parsed_date = parse(string, fuzzy=False)
        return parsed_date.strftime("%m/%d/%Y")
    except ValueError:
        return False


def is_currency(string: str) -> Union[bool, str]:
    """
    Check for currency
    """
    # todo: add more currency like euro, gdp, pounds
    search_res = re.search(r"$", string)
    if search_res:
        return string[search_res.start() : search_res.end()]  # noqa
    return False


type2func = {
    "amount": is_amount,
    "date": is_date,
    "object": is_object,
    "currency": is_currency,
    "fund_name": is_fund_name,
    "client_name": is_client_name,
    "no_fuzzy_date": convert_date,
}

default_mapping = MappingProxyType(type2func)


def process_answer(
    checking_type: str,
    answer: str,
    mapper: dict[str, Callable] = default_mapping,
) -> Union[str, None]:
    if checking_type not in mapper:
        return answer

    result = mapper[checking_type](answer)

    if not result:
        return

    result = result.strip()

    if len(result) <= 3:
        return

    if result[-1] in {",", ".", ":", ";", "!", "?"}:
        result = result[:-1]

    return result
