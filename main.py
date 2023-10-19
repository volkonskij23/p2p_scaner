from selenium                                import webdriver
from selenium.webdriver.common.by            import By
from selenium.webdriver.common.keys          import Keys
from selenium.webdriver.support.ui           import WebDriverWait
from selenium.webdriver.support              import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui           import Select
from webdriver_manager.chrome                import ChromeDriverManager
from bs4                                     import BeautifulSoup
from google.auth.transport.requests          import Request
from google.oauth2.credentials               import Credentials
from google_auth_oauthlib.flow               import InstalledAppFlow
from googleapiclient.discovery               import build
from oauth2client.service_account            import ServiceAccountCredentials
from websocket                               import create_connection
from datetime                                import datetime
import undetected_chromedriver               as uc
import json
import requests
import time
import httplib2
import apiclient.discovery
import pytz


"""
    Функция чтения json-файла

    :param     filename: Название файла
    :type      filename: str.
    
    :returns: dict или list
"""
def json_load(filename):
    with open(filename, "r", encoding="utf8") as read_file:
        result = json.load(read_file)
    return result

"""
    Функция записи в json-файл

    :param     filename: Название файла
    :type      filename: str.
    :param     data: Записываемые данные
    :type      data: list or dict.
  
"""
def json_dump(filename, data):
    with open(filename, "w", encoding="utf8") as write_file:
        json.dump(data, write_file, ensure_ascii=False)

"""
    Функция парсинга платежной системы Contact

    :returns: dict
  
"""
def contact(browser):

    curriencies = {}

    county_codes = {
        "AZ": ["AZN", "USD"],
        "GE": ["GEL", "USD"],
        "TJ": ["USD"],
        "TR": ["USD"],
        "UZ": ["USD"],
        "KZ": ["KZT", "USD"],
        "KG": ["USD"],
    }

    for code in county_codes.keys():
        url = "https://online.contact-sys.com/transfer/where?code={}".format(code)

        for currency in county_codes[code]:
            while True:
                try:
                    browser.get(url)
                    element = WebDriverWait(browser, 10).until(
                        EC.presence_of_element_located(
                            (
                                By.CLASS_NAME,
                                "css-s3gtbt-Component-StyledButton.edjgf0a0",
                            )
                        )
                    )

                    browser.find_element(
                        By.CLASS_NAME, "css-s3gtbt-Component-StyledButton.edjgf0a0"
                    ).click()

                    if code == "TR":
                        element = WebDriverWait(browser, 10).until(
                            EC.presence_of_element_located(
                                (
                                    By.CLASS_NAME,
                                    "css-s3gtbt-Component-StyledButton.edjgf0a0",
                                )
                            )
                        )

                        browser.find_element(
                            By.CLASS_NAME, "css-s3gtbt-Component-StyledButton.edjgf0a0"
                        ).click()

                    if code == "TH":
                        element = WebDriverWait(browser, 10).until(
                            EC.presence_of_element_located(
                                (
                                    By.CLASS_NAME,
                                    "ReactVirtualized__Table__row.css-iflrwy",
                                )
                            )
                        )

                        browser.find_element(
                            By.CLASS_NAME, "ReactVirtualized__Table__row.css-iflrwy"
                        ).click()

                        WebDriverWait(browser, 10).until(
                            EC.element_to_be_clickable(
                                (
                                    By.CLASS_NAME,
                                    "css-s3gtbt-Component-StyledButton.edjgf0a0",
                                )
                            )
                        ).click()

                    element = WebDriverWait(browser, 10).until(
                        EC.presence_of_element_located(
                            (By.CLASS_NAME, "css-1v6amd0-Control.eu2asnp1")
                        )
                    )

                    input_field = browser.find_element(
                        By.CLASS_NAME, "css-1v6amd0-Control.eu2asnp1"
                    )

                    input_field.send_keys("1000")

                    WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "css-ml0uk4"))
                    ).click()

                    element = WebDriverWait(browser, 10).until(
                        EC.presence_of_element_located(
                            (By.CLASS_NAME, "css-1s12ap7-menu")
                        )
                    )
                    select = browser.find_element(By.CLASS_NAME, "css-1s12ap7-menu")
                    names_block = select.find_elements(
                        By.CLASS_NAME, "css-1ig0jh2-TagElement.e1492quw0"
                    )

                    for name in names_block:

                        if name.text == currency:
                            name.click()
                            break

                    if code == "TH":
                        selects_block = browser.find_elements(
                            By.CLASS_NAME, "css-ml0uk4"
                        )

                        for block in selects_block[1:]:
                            WebDriverWait(browser, 10).until(
                                EC.element_to_be_clickable(block)
                            ).click()
                            element = WebDriverWait(browser, 10).until(
                                EC.presence_of_element_located(
                                    (By.CLASS_NAME, "css-1s12ap7-menu")
                                )
                            )

                            select = browser.find_element(
                                By.CLASS_NAME, "css-1s12ap7-menu"
                            )

                            names_block = select.find_elements(
                                By.CLASS_NAME, "css-1ig0jh2-TagElement.e1492quw0"
                            )
                            for name in names_block:
                                WebDriverWait(browser, 10).until(
                                    EC.element_to_be_clickable(name)
                                ).click()
                                break

                    WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable(
                            (
                                By.CLASS_NAME,
                                "css-s3gtbt-Component-StyledButton.edjgf0a0",
                            )
                        )
                    ).click()

                    element = WebDriverWait(browser, 10).until(
                        EC.presence_of_element_located(
                            (By.CLASS_NAME, "css-15yilgt-ValueSection.e11f1df53")
                        )
                    )

                    if currency != "KZT":
                        price = float(
                            browser.find_elements(
                                By.CLASS_NAME,
                                "e11f1df52.css-fea899-Component-TagElement-ValueWrapper.e110lpub0",
                            )[3]
                            .text.replace("1 {} = ".format(currency), "")
                            .replace(" RUB", "")
                        )
                    else:
                        price = 1 / float(
                            browser.find_elements(
                                By.CLASS_NAME,
                                "e11f1df52.css-fea899-Component-TagElement-ValueWrapper.e110lpub0",
                            )[3]
                            .text.replace("1 RUB = ", "")
                            .replace(" KZT", "")
                        )

                    key_name = code + "_" + currency
                    curriencies[key_name] = price
                    break
                except:
                    continue

    return curriencies


"""
    Функция парсинга платежной системы Unistream

    :returns: dict
  
"""
def unistream():
    curriencies = {}

    headers = json_load(r'./json/unistream_headers.json')

    curriencies["ARM_AMD_1"] = (
        requests.get(
            "https://online.unistream.ru/api/card2cash/calculate",
            params={
                "destination": "ARM",
                "amount": "1000",
                "currency": "AMD",
                "accepted_currency": "RUB",
                "profile": "unistream_front",
            },
            headers=headers,
        ).json()["fees"][0]["acceptedAmount"]
        / 1000
    )

    time.sleep(5)
    curriencies["ARM_USD_2"] = (
        requests.get(
            "https://online.unistream.ru/api/card2cash/calculate",
            params={
                "destination": "ARM",
                "amount": "1000",
                "currency": "USD",
                "accepted_currency": "RUB",
                "profile": "unistream_front",
            },
            headers=headers,
        ).json()["fees"][0]["acceptedAmount"]
        / 1000
    )
    time.sleep(5)
    curriencies["KAZ_KZT_3"] = (
        requests.get(
            "https://online.unistream.ru/api/card2cash/calculate",
            params={
                "destination": "KAZ",
                "amount": "1000",
                "currency": "KZT",
                "accepted_currency": "RUB",
                "profile": "unistream_front",
            },
            headers=headers,
        ).json()["fees"][0]["acceptedAmount"]
        / 1000
    )
    time.sleep(5)
    curriencies["MDA_USD_5"] = (
        requests.get(
            "https://online.unistream.ru/api/card2cash/calculate",
            params={
                "destination": "MDA",
                "amount": "1000",
                "currency": "USD",
                "accepted_currency": "RUB",
                "profile": "unistream_front",
            },
            headers=headers,
        ).json()["fees"][0]["acceptedAmount"]
        / 1000
    )
    time.sleep(5)
    curriencies["TJK_RUB_6"] = (
        requests.get(
            "https://online.unistream.ru/api/card2cash/calculate",
            params={
                "destination": "TJK",
                "amount": "10000",
                "currency": "RUB",
                "accepted_currency": "RUB",
                "profile": "unistream_front",
            },
            headers=headers,
        ).json()["fees"][0]["acceptedAmount"]
        / 10000
    )
    time.sleep(5)
    curriencies["UZB_UZS_7"] = (
        requests.get(
            "https://online.unistream.ru/api/card2cash/calculate",
            params={
                "destination": "UZB",
                "amount": "100000",
                "currency": "UZS",
                "accepted_currency": "RUB",
                "profile": "unistream_front",
                "payout_type": "card",
            },
            headers=headers,
        ).json()["fees"][0]["acceptedAmount"]
        / 100000
    )

    return curriencies


"""
    Функция парсинга платежной системы CoronaPay

    :returns: dict
  
"""
def coronapay():
    curriencies = {}

    cookies = json_load(r'./json/coronapay_cookies.json')

    headers = json_load(r'./json/coronapay_headers.json')

    cookies["_ga_H68H5PL1N6"] = "GS1.1.1692976149.1.1.{}.60.0.0".format(time.time())

    response = requests.get(
        "https://koronapay.com/transfers/online/api/transfers/tariffs",
        params={
            "sendingCountryId": "UZB",
            "sendingCurrencyId": "860",
            "receivingCountryId": "RUS",
            "receivingCurrencyId": "810",
            "paymentMethod": "debitCard",
            "receivingAmount": "100000",
            "receivingMethod": "cash",
            "paidNotificationEnabled": "false",
        },
        cookies=cookies,
        headers=headers,
    )
    curriencies["UZB_RUS_1"] = response.json()[0]["exchangeRate"]

    time.sleep(3)
    cookies["_ga_H68H5PL1N6"] = "GS1.1.1692976149.1.1.{}.60.0.0".format(time.time())

    curriencies["UZB_USD_2"] = requests.get(
        "https://koronapay.com/transfers/online/api/transfers/tariffs",
        params={
            "sendingCountryId": "RUS",
            "sendingCurrencyId": "810",
            "receivingCountryId": "UZB",
            "receivingCurrencyId": "840",
            "paymentMethod": "debitCard",
            "receivingAmount": "10000",
            "receivingMethod": "cash",
            "paidNotificationEnabled": "false",
        },
        cookies=cookies,
        headers=headers,
    ).json()[0]["exchangeRate"]
    time.sleep(3)
    cookies["_ga_H68H5PL1N6"] = "GS1.1.1692976149.1.1.{}.60.0.0".format(time.time())

    curriencies["KAZ_KZT_3"] = requests.get(
        "https://koronapay.com/transfers/online/api/transfers/tariffs",
        params={
            "sendingCountryId": "RUS",
            "sendingCurrencyId": "810",
            "receivingCountryId": "KAZ",
            "receivingCurrencyId": "398",
            "paymentMethod": "debitCard",
            "receivingAmount": "100000",
            "receivingMethod": "cash",
            "paidNotificationEnabled": "false",
        },
        cookies=cookies,
        headers=headers,
    ).json()[0]["exchangeRate"]
    time.sleep(3)
    cookies["_ga_H68H5PL1N6"] = "GS1.1.1692976149.1.1.{}.60.0.0".format(time.time())

    curriencies["KAZ_USD_4"] = requests.get(
        "https://koronapay.com/transfers/online/api/transfers/tariffs",
        params={
            "sendingCountryId": "RUS",
            "sendingCurrencyId": "810",
            "receivingCountryId": "KAZ",
            "receivingCurrencyId": "840",
            "paymentMethod": "debitCard",
            "receivingAmount": "100000",
            "receivingMethod": "cash",
            "paidNotificationEnabled": "false",
        },
        cookies=cookies,
        headers=headers,
    ).json()[0]["exchangeRate"]
    time.sleep(3)
    cookies["_ga_H68H5PL1N6"] = "GS1.1.1692976149.1.1.{}.60.0.0".format(time.time())

    curriencies["CHN_USD_5"] = requests.get(
        "https://koronapay.com/transfers/online/api/transfers/tariffs",
        params={
            "sendingCountryId": "RUS",
            "sendingCurrencyId": "810",
            "receivingCountryId": "CHN",
            "receivingCurrencyId": "840",
            "paymentMethod": "debitCard",
            "receivingAmount": "100000",
            "receivingMethod": "card",
            "paidNotificationEnabled": "false",
        },
        cookies=cookies,
        headers=headers,
    ).json()[0]["exchangeRate"]
    time.sleep(3)
    cookies["_ga_H68H5PL1N6"] = "GS1.1.1692976149.1.1.{}.60.0.0".format(time.time())

    curriencies["TJK_USD_6"] = requests.get(
        "https://koronapay.com/transfers/online/api/transfers/tariffs",
        params={
            "sendingCountryId": "RUS",
            "sendingCurrencyId": "810",
            "receivingCountryId": "TJK",
            "receivingCurrencyId": "840",
            "paymentMethod": "debitCard",
            "receivingAmount": "100",
            "receivingMethod": "cash",
            "paidNotificationEnabled": "false",
        },
        cookies=cookies,
        headers=headers,
    ).json()[0]["exchangeRate"]
    time.sleep(3)
    cookies["_ga_H68H5PL1N6"] = "GS1.1.1692976149.1.1.{}.60.0.0".format(time.time())

    curriencies["KGZ_USD_7"] = requests.get(
        "https://koronapay.com/transfers/online/api/transfers/tariffs",
        params={
            "sendingCountryId": "RUS",
            "sendingCurrencyId": "810",
            "receivingCountryId": "KGZ",
            "receivingCurrencyId": "840",
            "paymentMethod": "debitCard",
            "receivingAmount": "100000",
            "receivingMethod": "cash",
            "paidNotificationEnabled": "false",
        },
        cookies=cookies,
        headers=headers,
    ).json()[0]["exchangeRate"]
    time.sleep(3)
    cookies["_ga_H68H5PL1N6"] = "GS1.1.1692976149.1.1.{}.60.0.0".format(time.time())

    curriencies["AZE_AZN_8"] = requests.get(
        "https://koronapay.com/transfers/online/api/transfers/tariffs",
        params={
            "sendingCountryId": "RUS",
            "sendingCurrencyId": "810",
            "receivingCountryId": "AZE",
            "receivingCurrencyId": "944",
            "paymentMethod": "debitCard",
            "receivingAmount": "100000",
            "receivingMethod": "cash",
            "paidNotificationEnabled": "false",
        },
        cookies=cookies,
        headers=headers,
    ).json()[0]["exchangeRate"]
    time.sleep(3)
    cookies["_ga_H68H5PL1N6"] = "GS1.1.1692976149.1.1.{}.60.0.0".format(time.time())

    curriencies["AZE_USD_9"] = requests.get(
        "https://koronapay.com/transfers/online/api/transfers/tariffs",
        params={
            "sendingCountryId": "RUS",
            "sendingCurrencyId": "810",
            "receivingCountryId": "AZE",
            "receivingCurrencyId": "840",
            "paymentMethod": "debitCard",
            "receivingAmount": "100000",
            "receivingMethod": "cash",
            "paidNotificationEnabled": "false",
        },
        cookies=cookies,
        headers=headers,
    ).json()[0]["exchangeRate"]
    time.sleep(3)
    cookies["_ga_H68H5PL1N6"] = "GS1.1.1692976149.1.1.{}.60.0.0".format(time.time())

    curriencies["TUR_TRY_10"] = requests.get(
        "https://koronapay.com/transfers/online/api/transfers/tariffs",
        params={
            "sendingCountryId": "RUS",
            "sendingCurrencyId": "810",
            "receivingCountryId": "TUR",
            "receivingCurrencyId": "949",
            "paymentMethod": "debitCard",
            "receivingAmount": "100000",
            "receivingMethod": "cash",
            "paidNotificationEnabled": "false",
        },
        cookies=cookies,
        headers=headers,
    ).json()[0]["exchangeRate"]
    time.sleep(3)
    cookies["_ga_H68H5PL1N6"] = "GS1.1.1692976149.1.1.{}.60.0.0".format(time.time())

    curriencies["TUR_USD_11"] = requests.get(
        "https://koronapay.com/transfers/online/api/transfers/tariffs",
        params={
            "sendingCountryId": "RUS",
            "sendingCurrencyId": "810",
            "receivingCountryId": "TUR",
            "receivingCurrencyId": "840",
            "paymentMethod": "debitCard",
            "receivingAmount": "100000",
            "receivingMethod": "cash",
            "paidNotificationEnabled": "false",
        },
        cookies=cookies,
        headers=headers,
    ).json()[0]["exchangeRate"]
    time.sleep(3)
    cookies["_ga_H68H5PL1N6"] = "GS1.1.1692976149.1.1.{}.60.0.0".format(time.time())

    curriencies["MDA_MDL_12"] = requests.get(
        "https://koronapay.com/transfers/online/api/transfers/tariffs",
        params={
            "sendingCountryId": "RUS",
            "sendingCurrencyId": "810",
            "receivingCountryId": "MDA",
            "receivingCurrencyId": "498",
            "paymentMethod": "debitCard",
            "receivingAmount": "100000",
            "receivingMethod": "cash",
            "paidNotificationEnabled": "false",
        },
        cookies=cookies,
        headers=headers,
    ).json()[0]["exchangeRate"]
    time.sleep(3)
    cookies["_ga_H68H5PL1N6"] = "GS1.1.1692976149.1.1.{}.60.0.0".format(time.time())

    curriencies["MDA_USD_13"] = requests.get(
        "https://koronapay.com/transfers/online/api/transfers/tariffs",
        params={
            "sendingCountryId": "RUS",
            "sendingCurrencyId": "810",
            "receivingCountryId": "MDA",
            "receivingCurrencyId": "840",
            "paymentMethod": "debitCard",
            "receivingAmount": "100000",
            "receivingMethod": "cash",
            "paidNotificationEnabled": "false",
        },
        cookies=cookies,
        headers=headers,
    ).json()[0]["exchangeRate"]
    time.sleep(3)
    cookies["_ga_H68H5PL1N6"] = "GS1.1.1692976149.1.1.{}.60.0.0".format(time.time())

    curriencies["GEO_GEL_14"] = requests.get(
        "https://koronapay.com/transfers/online/api/transfers/tariffs",
        params={
            "sendingCountryId": "RUS",
            "sendingCurrencyId": "810",
            "receivingCountryId": "GEO",
            "receivingCurrencyId": "981",
            "paymentMethod": "debitCard",
            "receivingAmount": "100000",
            "receivingMethod": "cash",
            "paidNotificationEnabled": "false",
        },
        cookies=cookies,
        headers=headers,
    ).json()[0]["exchangeRate"]
    time.sleep(3)
    cookies["_ga_H68H5PL1N6"] = "GS1.1.1692976149.1.1.{}.60.0.0".format(time.time())

    curriencies["GEO_USD_15"] = requests.get(
        "https://koronapay.com/transfers/online/api/transfers/tariffs",
        params={
            "sendingCountryId": "RUS",
            "sendingCurrencyId": "810",
            "receivingCountryId": "GEO",
            "receivingCurrencyId": "840",
            "paymentMethod": "debitCard",
            "receivingAmount": "100000",
            "receivingMethod": "cash",
            "paidNotificationEnabled": "false",
        },
        cookies=cookies,
        headers=headers,
    ).json()[0]["exchangeRate"]
    time.sleep(3)
    cookies["_ga_H68H5PL1N6"] = "GS1.1.1692976149.1.1.{}.60.0.0".format(time.time())

    curriencies["VNM_USD_17"] = requests.get(
        "https://koronapay.com/transfers/online/api/transfers/tariffs",
        params={
            "sendingCountryId": "RUS",
            "sendingCurrencyId": "810",
            "receivingCountryId": "VNM",
            "receivingCurrencyId": "840",
            "paymentMethod": "debitCard",
            "receivingAmount": "100000",
            "receivingMethod": "cash",
            "paidNotificationEnabled": "false",
        },
        cookies=cookies,
        headers=headers,
    ).json()[0]["exchangeRate"]
    return curriencies


"""
    Функция парсинга платежной системы PaySend

    :returns: dict
  
"""
def paysend():
    curriencies = {}
    cookies = json_load(r'./json/paysend_cookies.json')

    headers = json_load(r'./json/paysend_headers.json')

    curriencies["UZS_KGS_1"] = float(
        requests.post(
            "https://paysend.com/api/ru-ro/otpravit-dengi/iz-uzbekistana-v-kyrgyzstan",
            params={
                "fromCurrId": "860",
                "toCurrId": "417",
                "isFrom": "true",
            },
            cookies=cookies,
            headers=headers,
        )
        .json()["paymentForm"]["currencyRateText"]
        .replace("1.00 KGS = ", "")
        .replace(" UZS", "")
    )
    curriencies["KZT_KGS_2"] = float(
        requests.post(
            "https://paysend.com/api/ru-ro/otpravit-dengi/iz-kazahstana-v-kyrgyzstan",
            params={
                "fromCurrId": "398",
                "toCurrId": "417",
                "isFrom": "true",
            },
            cookies=cookies,
            headers=headers,
        )
        .json()["paymentForm"]["currencyRateText"]
        .replace("1.00 KGS = ", "")
        .replace(" KZT", "")
    )
    return curriencies

"""
    Функция парсинга платежной системы MirPay

    :returns: dict
  
"""
def mirpay():
    curriencies = {}

    cookies = json_load(r'./json/mirpay_cookies.json')

    headers = json_load(r'./json/mirpay_headers.json')

    params = {
        "ELEMENT_CODE": "kursy_mir",
    }

    response = requests.get(
        "https://mironline.ru/support/list/kursy_mir/",
        params=params,
        cookies=cookies,
        headers=headers,
    )

    soup = BeautifulSoup(response.text, "html.parser")
    block = soup.find("div", class_="sf-text")

    trs = block.find_all("tr")

    for tr in trs[1:]:

        tds = tr.find_all("td")
        name = tds[0].text.strip()
        if name == "Армянский драм":
            curriencies["AMD_1"] = float(tds[1].text.strip().replace(",", "."))
        if name == "Белорусский рубль":
            curriencies["BYN_2"] = float(tds[1].text.strip().replace(",", "."))
        if name == "Венесуэльский боливар":
            curriencies["VES_3"] = float(tds[1].text.strip().replace(",", "."))
        if name == "Вьетнамский донг":
            curriencies["VND_4"] = float(tds[1].text.strip().replace(",", "."))
        if name == "Казахстанский тенге":
            curriencies["KZT_5"] = float(tds[1].text.strip().replace(",", "."))
        if name == "Кубинский песо":
            curriencies["CUP_6"] = float(tds[1].text.strip().replace(",", "."))
        if name == "Кыргызский сом":
            curriencies["KGS_7"] = float(tds[1].text.strip().replace(",", "."))
        if name == "Таджикский сомони":
            curriencies["TJS_8"] = float(tds[1].text.strip().replace(",", "."))
        if name == "Узбекский сум":
            curriencies["UZS_9"] = float(tds[1].text.strip().replace(",", "."))

    return curriencies




"""
    Функция парсинга спотовых котировок криптобиржи Binance
    
    :returns: dict
  
"""
def binance_spot():
    spot = requests.get("https://api.binance.com/api/v3/ticker/price").json()
    curriencies = {}
    spot_dict = {}

    for symbol in spot:
        spot_dict[symbol["symbol"]] = symbol["price"]

    curriencies["USDT_RUB_1"] = float(spot_dict["USDTRUB"])
    curriencies["BNB_RUB_1"] = float(spot_dict["BNBRUB"])
    curriencies["BTC_RUB_1"] = float(spot_dict["BTCRUB"])
    curriencies["ETH_RUB_1"] = float(spot_dict["ETHRUB"])
    curriencies["SOL_RUB_1"] = float(spot_dict["SOLRUB"])
    curriencies["BUSD_RUB_1"] = float(spot_dict["BUSDRUB"])
    curriencies["USDT_BTC_1"] = float(spot_dict["BTCUSDT"])
    curriencies["USDT_ETH_1"] = float(spot_dict["ETHUSDT"])
    curriencies["USDT_BNB_1"] = float(spot_dict["BNBUSDT"])
    curriencies["USDT_BUSD_1"] = float(spot_dict["BUSDUSDT"])

    return curriencies



""""
    Функция парсинга p2p-предложений криптобиржи Binance
    
    :param  operation_type: Тип операции (текйкер/мейкер - buy/sell)
    :type   operation_type: str.
    :param  coin: Наименование интересующей криптовалюты (USDT)
    :type   coin: str.
    :param  bank: Название инетерсующего банка для оплаты 
    :type   bank: str.
    :param  fiat: Название инетерсующей фиатной валюты
    :type   fiat: str
    
    :returns: float 
  
"""
def binance_fetchCryptoPricesFromApi(operation_type, coin, bank, fiat="RUB"):
    data = {
        "fiat": fiat,
        "page": 1,
        "rows": 10,
        "tradeType": operation_type,
        "asset": coin,
        "countries": [],
        "proMerchantAds": False,
        "publisherType": None,
        "payTypes": [bank],
    }

    cookies = json_load(r"./json/binance_cookies.json")
    headers = json_load(r"./json/binance_headers.json")

    prices = requests.post(
        "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search",
        cookies=cookies,
        headers=headers,
        data=json.dumps(data),
    ).json()["data"]

    count = 0
    avg_price = 0

    for price in prices:
        avg_price += float(price["adv"]["price"])
        count += 1
        if count == 3:
            break

    return avg_price / count if count != 0 else 0


""""
    Функция парсинга p2p-предложений криптобиржи Bybit
    
    :param  operation_type: Тип операции (текйкер/мейкер - 1/0)
    :type   operation_type: str.
    :param  coin: Наименование интересующей криптовалюты (USDT)
    :type   coin: str.
    :param  bank: Название инетерсующего банка для оплаты 
    :type   bank: str.
    
    :returns: float 
  
"""
def bybit_fetchCryptoPricesFromApi(operation_type, coin, bank):
    
    bank_ids = {
        "TinkoffNew": 75,
        "RosBankNew": 185,
        "QIWI": 62,
        "YandexMoneyNew": 274,
        "RaiffeisenBank": 64,
    }
    data = {
        "userId": "67004610",
        "tokenId": coin,
        "currencyId": "RUB",
        "payment": [str(bank_ids[bank])],
        "side": str(operation_type),
        "size": "10",
        "page": "1",
        "amount": "",
        "authMaker": False,
        "canTrade": False,
    }
    cookies = json_load(r'./json/bybit_cookies.json')

    headers = json_load(r'./json/bybit_headers.json')

    prices = requests.post(
        "https://api2.bybit.com/fiat/otc/item/online",
        cookies=cookies,
        headers=headers,
        data=json.dumps(data),
    ).json()["result"]["items"]

    count = 0
    avg_price = 0

    for price in prices:
        avg_price += float(price["price"])
        count += 1
        if count == 3:
            break

    return avg_price / count if count != 0 else 0


""""
    Функция парсинга p2p-предложений криптобиржи OKX
    
    :param  operation_type: Тип операции (текйкер/мейкер -buy/sell)
    :type   operation_type: str.
    :param  coin: Наименование интересующей криптовалюты (USDT)
    :type   coin: str.
    :param  bank: Название инетерсующего банка для оплаты 
    :type   bank: str.
    
    :returns: float 
  
"""

def okx_fetchCryptoPricesFromApi(operation_type, coin, bank):
   
    cookies = json_load(r'./json/okx_cookies.json')

    headers = json_load(r'./json/okx_headers.json')

    params = {
        "t": str(int(time.time())),
        "side": operation_type,
        "paymentMethod": bank,
        "userType": "all",
        "hideOverseasVerificationAds": "false",
        "sortType": "price_asc" if operation_type == "sell" else "price_desc",
        "urlId": "4",
        "limit": "100",
        "cryptoCurrency": coin,
        "fiatCurrency": "rub",
        "currentPage": "1",
        "numberPerPage": "5",
    }

    prices = requests.get(
        "https://www.okx.com/v3/c2c/tradingOrders/getMarketplaceAdsPrelogin",
        params=params,
        cookies=cookies,
        headers=headers,
    ).json()["data"][operation_type]

    count = 0
    avg_price = 0

    for price in prices:
        avg_price += float(price["price"])
        count += 1
        if count == 3:
            break

    return avg_price / count if count != 0 else 0


""""
    Функция формирования словаря с результатами парсинга криптобиржы OKX
    
    :returns: dict 
  
"""

def okx_p2p():
    curriencies = {}

    # Rife
    curriencies["RaiffeisenBank_buy_USDT_T"] = round(
        okx_fetchCryptoPricesFromApi("sell", "USDT", "Raiffaizen"), 4
    )
    curriencies["RaiffeisenBank_sell_USDT_T"] = round(
        okx_fetchCryptoPricesFromApi("buy", "USDT", "Raiffaizen"), 4
    )

    curriencies["RaiffeisenBank_buy_BTC_T"] = round(
        okx_fetchCryptoPricesFromApi("sell", "BTC", "Raiffaizen"), 4
    )
    curriencies["RaiffeisenBank_sell_BTC_T"] = round(
        okx_fetchCryptoPricesFromApi("buy", "BTC", "Raiffaizen"), 4
    )

    curriencies["RaiffeisenBank_buy_ETH_T"] = round(
        okx_fetchCryptoPricesFromApi("sell", "ETH", "Raiffaizen"), 4
    )
    curriencies["RaiffeisenBank_sell_ETH_T"] = round(
        okx_fetchCryptoPricesFromApi("buy", "ETH", "Raiffaizen"), 4
    )

    #  QIWI
    curriencies["QIWI_buy_USDT_T"] = round(
        okx_fetchCryptoPricesFromApi("sell", "USDT", "QiWi"), 4
    )
    curriencies["QIWI_sell_USDT_T"] = round(
        okx_fetchCryptoPricesFromApi("buy", "USDT", "QiWi"), 4
    )

    curriencies["QIWI_buy_BTC_T"] = round(
        okx_fetchCryptoPricesFromApi("sell", "BTC", "QiWi"), 4
    )
    curriencies["QIWI_sell_BTC_T"] = round(
        okx_fetchCryptoPricesFromApi("buy", "BTC", "QiWi"), 4
    )

    curriencies["QIWI_buy_ETH_T"] = round(
        okx_fetchCryptoPricesFromApi("sell", "ETH", "QiWi"), 4
    )
    curriencies["QIWI_sell_ETH_T"] = round(
        okx_fetchCryptoPricesFromApi("buy", "ETH", "QiWi"), 4
    )

    # Yandex
    curriencies["YandexMoneyNew_buy_USDT_T"] = round(
        okx_fetchCryptoPricesFromApi("sell", "USDT", "Yandex.Money"), 4
    )
    curriencies["YandexMoneyNew_sell_USDT_T"] = round(
        okx_fetchCryptoPricesFromApi("buy", "USDT", "Yandex.Money"), 4
    )

    curriencies["YandexMoneyNew_buy_BTC_T"] = round(
        okx_fetchCryptoPricesFromApi("sell", "BTC", "Yandex.Money"), 4
    )
    curriencies["YandexMoneyNew_sell_BTC_T"] = round(
        okx_fetchCryptoPricesFromApi("buy", "BTC", "Yandex.Money"), 4
    )

    curriencies["YandexMoneyNew_buy_ETH_T"] = round(
        okx_fetchCryptoPricesFromApi("sell", "ETH", "Yandex.Money"), 4
    )
    curriencies["YandexMoneyNew_sell_ETH_T"] = round(
        okx_fetchCryptoPricesFromApi("buy", "ETH", "Yandex.Money"), 4
    )

    # Rosbank
    curriencies["RussianStandardBank_buy_USDT_T"] = round(
        okx_fetchCryptoPricesFromApi("sell", "USDT", "Sberbank"), 4
    )
    curriencies["RussianStandardBank_sell_USDT_T"] = round(
        okx_fetchCryptoPricesFromApi("buy", "USDT", "Sberbank"), 4
    )

    curriencies["RussianStandardBank_buy_BTC_T"] = round(
        okx_fetchCryptoPricesFromApi("sell", "BTC", "Sberbank"), 4
    )
    curriencies["RussianStandardBank_sell_BTC_T"] = round(
        okx_fetchCryptoPricesFromApi("buy", "BTC", "Sberbank"), 4
    )

    curriencies["RussianStandardBank_buy_ETH_T"] = round(
        okx_fetchCryptoPricesFromApi("sell", "ETH", "Sberbank"), 4
    )
    curriencies["RussianStandardBank_sell_ETH_T"] = round(
        okx_fetchCryptoPricesFromApi("buy", "ETH", "Sberbank"), 4
    )

    # Tink
    curriencies["RaiffeisenBankAval_buy_USDT_T"] = round(
        okx_fetchCryptoPricesFromApi("sell", "USDT", "Tinkoff"), 4
    )
    curriencies["RaiffeisenBankAval_sell_USDT_T"] = round(
        okx_fetchCryptoPricesFromApi("buy", "USDT", "Tinkoff"), 4
    )

    curriencies["RaiffeisenBankAval_buy_BTC_T"] = round(
        okx_fetchCryptoPricesFromApi("sell", "BTC", "Tinkoff"), 4
    )
    curriencies["RaiffeisenBankAval_sell_BTC_T"] = round(
        okx_fetchCryptoPricesFromApi("buy", "BTC", "Tinkoff"), 4
    )

    curriencies["RaiffeisenBankAval_buy_ETH_T"] = round(
        okx_fetchCryptoPricesFromApi("sell", "ETH", "Tinkoff"), 4
    )
    curriencies["RaiffeisenBankAval_sell_ETH_T"] = round(
        okx_fetchCryptoPricesFromApi("buy", "ETH", "Tinkoff"), 4
    )

    return curriencies

""""
    Функция формирования словаря с результатами парсинга криптобиржы ByBit
    
    :returns: dict 
  
"""
def bybit_p2p():
    curriencies = {}

    # Rife
    curriencies["RaiffeisenBank_buy_USDT_T"] = round(
        bybit_fetchCryptoPricesFromApi(1, "USDT", "RaiffeisenBank"), 4
    )
    curriencies["RaiffeisenBank_sell_USDT_T"] = round(
        bybit_fetchCryptoPricesFromApi(0, "USDT", "RaiffeisenBank"), 4
    )

    curriencies["RaiffeisenBank_buy_BTC_T"] = round(
        bybit_fetchCryptoPricesFromApi(1, "BTC", "RaiffeisenBank"), 4
    )
    curriencies["RaiffeisenBank_sell_BTC_T"] = round(
        bybit_fetchCryptoPricesFromApi(0, "BTC", "RaiffeisenBank"), 4
    )

    curriencies["RaiffeisenBank_buy_ETH_T"] = round(
        bybit_fetchCryptoPricesFromApi(1, "ETH", "RaiffeisenBank"), 4
    )
    curriencies["RaiffeisenBank_sell_ETH_T"] = round(
        bybit_fetchCryptoPricesFromApi(0, "ETH", "RaiffeisenBank"), 4
    )

    #  QIWI
    curriencies["QIWI_buy_USDT_T"] = round(
        bybit_fetchCryptoPricesFromApi(1, "USDT", "QIWI"), 4
    )
    curriencies["QIWI_sell_USDT_T"] = round(
        bybit_fetchCryptoPricesFromApi(0, "USDT", "QIWI"), 4
    )

    curriencies["QIWI_buy_BTC_T"] = round(
        bybit_fetchCryptoPricesFromApi(1, "BTC", "QIWI"), 4
    )
    curriencies["QIWI_sell_BTC_T"] = round(
        bybit_fetchCryptoPricesFromApi(0, "BTC", "QIWI"), 4
    )

    curriencies["QIWI_buy_ETH_T"] = round(
        bybit_fetchCryptoPricesFromApi(1, "ETH", "QIWI"), 4
    )
    curriencies["QIWI_sell_ETH_T"] = round(
        bybit_fetchCryptoPricesFromApi(0, "ETH", "QIWI"), 4
    )

    # Yandex
    curriencies["YandexMoneyNew_buy_USDT_T"] = round(
        bybit_fetchCryptoPricesFromApi(1, "USDT", "YandexMoneyNew"), 4
    )
    curriencies["YandexMoneyNew_sell_USDT_T"] = round(
        bybit_fetchCryptoPricesFromApi(0, "USDT", "YandexMoneyNew"), 4
    )

    curriencies["YandexMoneyNew_buy_BTC_T"] = round(
        bybit_fetchCryptoPricesFromApi(1, "BTC", "YandexMoneyNew"), 4
    )
    curriencies["YandexMoneyNew_sell_BTC_T"] = round(
        bybit_fetchCryptoPricesFromApi(0, "BTC", "YandexMoneyNew"), 4
    )

    curriencies["YandexMoneyNew_buy_ETH_T"] = round(
        bybit_fetchCryptoPricesFromApi(1, "ETH", "YandexMoneyNew"), 4
    )
    curriencies["YandexMoneyNew_sell_ETH_T"] = round(
        bybit_fetchCryptoPricesFromApi(0, "ETH", "YandexMoneyNew"), 4
    )

    # # Rosbank
    # curriencies['RussianStandardBank_buy_USDT_T']  = round(bybit_fetchCryptoPricesFromApi(1,"USDT", "RosBankNew"),4)
    # curriencies['RussianStandardBank_sell_USDT_T'] = round(bybit_fetchCryptoPricesFromApi(0,"USDT", "RosBankNew"),4)

    # curriencies['RussianStandardBank_buy_BTC_T'] = round(bybit_fetchCryptoPricesFromApi(1,"BTC", "RosBankNew"),4)
    # curriencies['RussianStandardBank_sell_BTC_T'] = round(bybit_fetchCryptoPricesFromApi(0,"BTC", "RosBankNew"),4)

    # curriencies['RussianStandardBank_buy_ETH_T'] = round(bybit_fetchCryptoPricesFromApi(1,"ETH", "RosBankNew"),4)
    # curriencies['RussianStandardBank_sell_ETH_T'] = round(bybit_fetchCryptoPricesFromApi(0,"ETH", "RosBankNew"),4)

    # #Tink
    # curriencies['RaiffeisenBankAval_buy_USDT_T']  = round(bybit_fetchCryptoPricesFromApi(1,"USDT", "TinkoffNew"),4)
    # curriencies['RaiffeisenBankAval_sell_USDT_T'] = round(bybit_fetchCryptoPricesFromApi(0,"USDT", "TinkoffNew"),4)

    # curriencies['RaiffeisenBankAval_buy_BTC_T'] = round(bybit_fetchCryptoPricesFromApi(1,"BTC", "TinkoffNew"),4)
    # curriencies['RaiffeisenBankAval_sell_BTC_T'] = round(bybit_fetchCryptoPricesFromApi(0,"BTC", "TinkoffNew"),4)

    # curriencies['RaiffeisenBankAval_buy_ETH_T'] = round(bybit_fetchCryptoPricesFromApi(1,"ETH", "TinkoffNew"),4)
    # curriencies['RaiffeisenBankAval_sell_ETH_T'] = round(bybit_fetchCryptoPricesFromApi(0,"ETH", "TinkoffNew"),4)

    return curriencies


""""
    Функция формирования словаря с результатами парсинга криптобиржы Binance с фиатом RUB
    
    :returns: dict 
  
"""
def binance_p2p():
    curriencies = {}

    # Rife
    curriencies["RaiffeisenBank_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "RaiffeisenBank"), 4
    )
    curriencies["RaiffeisenBank_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "RaiffeisenBank"), 4
    )

    curriencies["RaiffeisenBank_buy_BTC_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "BTC", "RaiffeisenBank"), 4
    )
    curriencies["RaiffeisenBank_sell_BTC_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "BTC", "RaiffeisenBank"), 4
    )

    curriencies["RaiffeisenBank_buy_BUSD_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "BUSD", "RaiffeisenBank"), 4
    )
    curriencies["RaiffeisenBank_sell_BUSD_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "BUSD", "RaiffeisenBank"), 4
    )

    curriencies["RaiffeisenBank_buy_BNB_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "BNB", "RaiffeisenBank"), 4
    )
    curriencies["RaiffeisenBank_sell_BNB_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "BNB", "RaiffeisenBank"), 4
    )

    curriencies["RaiffeisenBank_buy_ETH_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "ETH", "RaiffeisenBank"), 4
    )
    curriencies["RaiffeisenBank_sell_ETH_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "ETH", "RaiffeisenBank"), 4
    )

    curriencies["RaiffeisenBank_buy_RUB_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "RUB", "RaiffeisenBank"), 4
    )
    curriencies["RaiffeisenBank_sell_RUB_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "RUB", "RaiffeisenBank"), 4
    )

    #  QIWI
    curriencies["QIWI_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "QIWI"), 4
    )
    curriencies["QIWI_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "QIWI"), 4
    )

    curriencies["QIWI_buy_BTC_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "BTC", "QIWI"), 4
    )
    curriencies["QIWI_sell_BTC_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "BTC", "QIWI"), 4
    )

    curriencies["QIWI_buy_BUSD_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "BUSD", "QIWI"), 4
    )
    curriencies["QIWI_sell_BUSD_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "BUSD", "QIWI"), 4
    )

    curriencies["QIWI_buy_BNB_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "BNB", "QIWI"), 4
    )
    curriencies["QIWI_sell_BNB_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "BNB", "QIWI"), 4
    )

    curriencies["QIWI_buy_ETH_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "ETH", "QIWI"), 4
    )
    curriencies["QIWI_sell_ETH_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "ETH", "QIWI"), 4
    )

    curriencies["QIWI_buy_RUB_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "RUB", "QIWI"), 4
    )
    curriencies["QIWI_sell_RUB_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "RUB", "QIWI"), 4
    )

    # Yandex
    curriencies["YandexMoneyNew_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "YandexMoneyNew"), 4
    )
    curriencies["YandexMoneyNew_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "YandexMoneyNew"), 4
    )

    curriencies["YandexMoneyNew_buy_BTC_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "BTC", "YandexMoneyNew"), 4
    )
    curriencies["YandexMoneyNew_sell_BTC_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "BTC", "YandexMoneyNew"), 4
    )

    curriencies["YandexMoneyNew_buy_BUSD_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "BUSD", "YandexMoneyNew"), 4
    )
    curriencies["YandexMoneyNew_sell_BUSD_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "BUSD", "YandexMoneyNew"), 4
    )

    curriencies["YandexMoneyNew_buy_BNB_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "BNB", "YandexMoneyNew"), 4
    )
    curriencies["YandexMoneyNew_sell_BNB_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "BNB", "YandexMoneyNew"), 4
    )

    curriencies["YandexMoneyNew_buy_ETH_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "ETH", "YandexMoneyNew"), 4
    )
    curriencies["YandexMoneyNew_sell_ETH_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "ETH", "YandexMoneyNew"), 4
    )

    curriencies["YandexMoneyNew_buy_RUB_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "RUB", "YandexMoneyNew"), 4
    )
    curriencies["YandexMoneyNew_sell_RUB_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "RUB", "YandexMoneyNew"), 4
    )

    # Rosbank
    curriencies["RussianStandardBank_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "RussianStandardBank"), 4
    )
    curriencies["RussianStandardBank_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "RussianStandardBank"), 4
    )

    curriencies["RussianStandardBank_buy_BTC_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "BTC", "RussianStandardBank"), 4
    )
    curriencies["RussianStandardBank_sell_BTC_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "BTC", "RussianStandardBank"), 4
    )

    curriencies["RussianStandardBank_buy_BUSD_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "BUSD", "RussianStandardBank"), 4
    )
    curriencies["RussianStandardBank_sell_BUSD_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "BUSD", "RussianStandardBank"), 4
    )

    curriencies["RussianStandardBank_buy_BNB_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "BNB", "RussianStandardBank"), 4
    )
    curriencies["RussianStandardBank_sell_BNB_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "BNB", "RussianStandardBank"), 4
    )

    curriencies["RussianStandardBank_buy_ETH_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "ETH", "RussianStandardBank"), 4
    )
    curriencies["RussianStandardBank_sell_ETH_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "ETH", "RussianStandardBank"), 4
    )

    curriencies["RussianStandardBank_buy_RUB_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "RUB", "RussianStandardBank"), 4
    )
    curriencies["RussianStandardBank_sell_RUB_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "RUB", "RussianStandardBank"), 4
    )

    # Tink
    # curriencies['RaiffeisenBankAval_buy_USDT_T']  = round(binance_fetchCryptoPricesFromApi("buy","USDT", "RaiffeisenBankAval"),4)
    # curriencies['RaiffeisenBankAval_sell_USDT_T'] = round(binance_fetchCryptoPricesFromApi("sell","USDT", "RaiffeisenBankAval"),4)

    # curriencies['RaiffeisenBankAval_buy_BTC_T'] = round(binance_fetchCryptoPricesFromApi("buy","BTC", "RaiffeisenBankAval"),4)
    # curriencies['RaiffeisenBankAval_sell_BTC_T'] = round(binance_fetchCryptoPricesFromApi("sell","BTC", "RaiffeisenBankAval"),4)

    # curriencies['RaiffeisenBankAval_buy_BUSD_T'] = round(binance_fetchCryptoPricesFromApi("buy","BUSD", "RaiffeisenBankAval"),4)
    # curriencies['RaiffeisenBankAval_sell_BUSD_T'] = round(binance_fetchCryptoPricesFromApi("sell","BUSD", "RaiffeisenBankAval"),4)

    # curriencies['RaiffeisenBankAval_buy_BNB_T'] = round(binance_fetchCryptoPricesFromApi("buy","BNB", "RaiffeisenBankAval"),4)
    # curriencies['RaiffeisenBankAval_sell_BNB_T'] = round(binance_fetchCryptoPricesFromApi("sell","BNB", "RaiffeisenBankAval"),4)

    # curriencies['RaiffeisenBankAval_buy_ETH_T'] = round(binance_fetchCryptoPricesFromApi("buy","ETH", "RaiffeisenBankAval"),4)
    # curriencies['RaiffeisenBankAval_sell_ETH_T'] = round(binance_fetchCryptoPricesFromApi("sell","ETH", "RaiffeisenBankAval"),4)

    # curriencies['RaiffeisenBankAval_buy_RUB_T'] = round(binance_fetchCryptoPricesFromApi("buy","RUB", "RaiffeisenBankAval"),4)
    # curriencies['RaiffeisenBankAval_sell_RUB_T'] = round(binance_fetchCryptoPricesFromApi("sell","RUB", "RaiffeisenBankAval"),4)

    return curriencies


""""
    Функция формирования словаря с результатами парсинга криптобиржы Binance с фиатом UZS
    
    :returns: dict 
  
"""
def binance_p2p_uzs():
    curriencies = {}

    # Humo
    curriencies["Humo_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "Humo", "UZS"), 4
    )
    curriencies["Humo_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "Humo", "UZS"), 4
    )

    #  Uzcard
    curriencies["Uzcard_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "Uzcard", "UZS"), 4
    )
    curriencies["Uzcard_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "Uzcard", "UZS"), 4
    )

    # Kapitalbank
    curriencies["Kapitalbank_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "Kapitalbank", "UZS"), 4
    )
    curriencies["Kapitalbank_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "Kapitalbank", "UZS"), 4
    )

    # Rosbank
    curriencies["UzbekNationalBank_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "UzbekNationalBank", "UZS"), 4
    )
    curriencies["UzbekNationalBank_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "UzbekNationalBank", "UZS"), 4
    )

    return curriencies


""""
    Функция формирования словаря с результатами парсинга криптобиржы Binance с фиатом KGS
    
    :returns: dict 
  
"""
def binance_p2p_kgs():
    curriencies = {}

    # mBank
    curriencies["mBank_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "mBank", "KGS"), 4
    )
    curriencies["mBank_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "mBank", "KGS"), 4
    )

    #  OPTIMABANK
    curriencies["OPTIMABANK_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "OPTIMABANK", "KGS"), 4
    )
    curriencies["OPTIMABANK_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "OPTIMABANK", "KGS"), 4
    )

    # ELCART
    curriencies["ELCART_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "ELCART", "KGS"), 4
    )
    curriencies["ELCART_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "ELCART", "KGS"), 4
    )

    # DEMIRBANK
    curriencies["DEMIRBANK_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "DEMIRBANK", "KGS"), 4
    )
    curriencies["DEMIRBANK_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "DEMIRBANK", "KGS"), 4
    )

    return curriencies


""""
    Функция формирования словаря с результатами парсинга криптобиржы Binance с фиатом KZT
    
    :returns: dict 
  
"""
def binance_p2p_kzt():
    curriencies = {}

    # KaspiBank
    curriencies["KaspiBank_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "KaspiBank", "KZT"), 4
    )
    curriencies["KaspiBank_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "KaspiBank", "KZT"), 4
    )

    #  AltynBank
    curriencies["AltynBank_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "AltynBank", "KZT"), 4
    )
    curriencies["AltynBank_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "AltynBank", "KZT"), 4
    )

    # BankRBK
    curriencies["BankRBK_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "BankRBK", "KZT"), 4
    )
    curriencies["BankRBK_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "BankRBK", "KZT"), 4
    )

    # EurasianBank
    curriencies["EurasianBank_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "EurasianBank", "KZT"), 4
    )
    curriencies["EurasianBank_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "EurasianBank", "KZT"), 4
    )

    return curriencies


""""
    Функция формирования словаря с результатами парсинга криптобиржы Binance с фиатом TRY
    
    :returns: dict 
  
"""
def binance_p2p_try():
    curriencies = {}

    # VakifBank
    curriencies["VakifBank_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "VakifBank", "TRY"), 4
    )
    curriencies["VakifBank_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "VakifBank", "TRY"), 4
    )

    #  ISBANK
    curriencies["ISBANK_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "ISBANK", "TRY"), 4
    )
    curriencies["ISBANK_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "ISBANK", "TRY"), 4
    )

    # QNB
    curriencies["QNB_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "QNB", "TRY"), 4
    )
    curriencies["QNB_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "QNB", "TRY"), 4
    )

    # Ziraat
    curriencies["Ziraat_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "Ziraat", "TRY"), 4
    )
    curriencies["Ziraat_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "Ziraat", "TRY"), 4
    )

    return curriencies


""""
    Функция формирования словаря с результатами парсинга криптобиржы Binance с фиатом GEL
    
    :returns: dict 
  
"""
def binance_p2p_gel():
    curriencies = {}

    fiat = "GEL"
    #
    curriencies["bank1_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "CREDOBANK", fiat), 4
    )
    curriencies["bank1_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "CREDOBANK", fiat), 4
    )

    #
    curriencies["bank2_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "TBCbank", fiat), 4
    )
    curriencies["bank2_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "TBCbank", fiat), 4
    )

    #
    curriencies["bank3_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "BankofGeorgia", fiat), 4
    )
    curriencies["bank3_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "BankofGeorgia", fiat), 4
    )

    #
    curriencies["bank4_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "BASISBANK", fiat), 4
    )
    curriencies["bank4_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "BASISBANK", fiat), 4
    )

    return curriencies


""""
    Функция формирования словаря с результатами парсинга криптобиржы Binance с фиатом TJS
    
    :returns: dict 
  
"""
def binance_p2p_tjs():
    curriencies = {}

    fiat = "TJS"
    #
    curriencies["bank1_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "AlifBank", fiat), 4
    )
    curriencies["bank1_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "AlifBank", fiat), 4
    )

    #
    curriencies["bank2_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "SpitamenBank", fiat), 4
    )
    curriencies["bank2_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "SpitamenBank", fiat), 4
    )

    #
    curriencies["bank3_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "DCbank", fiat), 4
    )
    curriencies["bank3_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "DCbank", fiat), 4
    )

    #
    curriencies["bank4_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "BankEskhata", fiat), 4
    )
    curriencies["bank4_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "BankEskhata", fiat), 4
    )

    return curriencies


""""
    Функция формирования словаря с результатами парсинга криптобиржы Binance с фиатом AMD
    
    :returns: dict 
  
"""
def binance_p2p_amd():
    curriencies = {}

    fiat = "AMD"
    #
    curriencies["bank1_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "IDBank", fiat), 4
    )
    curriencies["bank1_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "IDBank", fiat), 4
    )

    #
    curriencies["bank2_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "Ardshinbank", fiat), 4
    )
    curriencies["bank2_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "Ardshinbank", fiat), 4
    )

    #
    curriencies["bank3_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "BANK", fiat), 4
    )
    curriencies["bank3_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "BANK", fiat), 4
    )

    #
    curriencies["bank4_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "ArCA", fiat), 4
    )
    curriencies["bank4_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "ArCA", fiat), 4
    )

    return curriencies


""""
    Функция формирования словаря с результатами парсинга криптобиржы Binance с фиатом AZN
    
    :returns: dict 
  
"""
def binance_p2p_azn():
    curriencies = {}

    fiat = "AZN"
    #
    curriencies["bank1_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "m10", fiat), 4
    )
    curriencies["bank1_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "m10", fiat), 4
    )

    #
    curriencies["bank2_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "ABBBANK", fiat), 4
    )
    curriencies["bank2_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "ABBBANK", fiat), 4
    )

    #
    curriencies["bank3_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "Kapitalbank", fiat), 4
    )
    curriencies["bank3_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "Kapitalbank", fiat), 4
    )

    #
    curriencies["bank4_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "LeoBank", fiat), 4
    )
    curriencies["bank4_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "LeoBank", fiat), 4
    )

    return curriencies

""""
    Функция формирования словаря с результатами парсинга криптобиржы Binance с фиатом MDL
    
    :returns: dict 
  
"""
def binance_p2p_mdl():
    curriencies = {}

    fiat = "MDL"
    #
    curriencies["bank1_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "FinComBank", fiat), 4
    )
    curriencies["bank1_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "FinComBank", fiat), 4
    )

    #
    curriencies["bank2_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "Victoriabank", fiat), 4
    )
    curriencies["bank2_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "Victoriabank", fiat), 4
    )

    #
    curriencies["bank3_buy_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("buy", "USDT", "MAIB", fiat), 4
    )
    curriencies["bank3_sell_USDT_T"] = round(
        binance_fetchCryptoPricesFromApi("sell", "USDT", "MAIB", fiat), 4
    )

    return curriencies


""""
    Функция парсинга криптобиржы Beribit с использованием websockets
    
    :returns: dict 
  
"""
def beribit():
    curriencies = {}

    headers =  cookies = json_load(r"./json/beribit_cookies.json")
    ws = create_connection("wss://beribit.com/ws/exchange_prices", header=headers)
    result = json.loads(ws.recv())

    curriencies["USDT_RUB"] = result["USDT_RUB"]["ExchangeRate"]
    curriencies["ETH_USDT"] = result["ETH_USDT"]["ExchangeRate"]
    curriencies["BTC_USDT"] = result["BTC_USDT"]["ExchangeRate"]
    curriencies["BNB_USDT"] = result["BNB_USDT"]["ExchangeRate"]
    ws.close()
    return curriencies


""""
    Функция импорта данных, полчуенных парсингом криптобиржы Beribit в гугл-таблицу
  
"""
def beribit_udpate(service):
    pay_curriencies = beribit()

    body = {
        "values": [
            [
                pay_curriencies["USDT_RUB"],
                "",
                "",
                "",
                "",
                "",
                pay_curriencies["BTC_USDT"],
                pay_curriencies["ETH_USDT"],
                pay_curriencies["BNB_USDT"],
            ],
        ]
    }
    SAMPLE_RANGE_NAME = "Котировки!B52"

    service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()


""""
    Функция парсинга спотовых котировок криптобиржи Garantex
    
    :returns: dict 
  
"""
def garantex():
    curriencies = {}

    curr_list = ["usdtrub", "btcrub", "ethrub", "btcusdt", "ethusdt"]

    for curr in curr_list:

        curriencies[curr] = requests.get(
            "https://garantex.org/api/v2/depth?market={}".format(curr)
        ).json()["asks"][0]["price"]

    return curriencies

"""
    Функция импорта данных, полчуенных парсингом спотовых котировок криптобиржы Garantex в гугл-таблицу
  
"""
def garantex_spot_update(service):
    pay_curriencies = garantex()

    body = {
        "values": [
            [
                pay_curriencies["usdtrub"],
                "",
                pay_curriencies["btcrub"],
                pay_curriencies["ethrub"],
                "",
                "",
                pay_curriencies["btcusdt"],
                pay_curriencies["ethusdt"],
            ],
        ]
    }

    SAMPLE_RANGE_NAME = "Котировки!B50"

    service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()



"""
    Функция импорта данных, полчуенных парсингом платежной системы MirPay в гугл-таблицу
  
"""
def mirpay_update(service):

    mir_pay_curriencies = mirpay()

    mir_body = {
        "values": [
            [mir_pay_curriencies["AMD_1"]],
            [mir_pay_curriencies["BYN_2"]],
            [mir_pay_curriencies["VES_3"]],
            [mir_pay_curriencies["VND_4"]],
            [mir_pay_curriencies["KZT_5"]],
            [mir_pay_curriencies["CUP_6"]],
            [mir_pay_curriencies["KGS_7"]],
            [mir_pay_curriencies["TJS_8"]],
            [mir_pay_curriencies["UZS_9"]],
        ]
    }

    SAMPLE_RANGE_NAME = "Котировки!C92"

    service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME,
        valueInputOption="USER_ENTERED",
        body=mir_body,
    ).execute()


"""
    Функция импорта данных, полчуенных парсингом платежной системы Unistream в гугл-таблицу
  
"""
def unistream_update(service):

    pay_curriencies = unistream()

    body = {
        "values": [
            [pay_curriencies["ARM_AMD_1"]],
            [pay_curriencies["ARM_USD_2"]],
            [pay_curriencies["KAZ_KZT_3"]],
            [],
            [pay_curriencies["MDA_USD_5"]],
            [pay_curriencies["TJK_RUB_6"]],
            [pay_curriencies["UZB_UZS_7"]],
        ]
    }

    SAMPLE_RANGE_NAME = "Котировки!K3"

    service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()

"""
    Функция импорта данных, полчуенных парсингом платежной системы Contact в гугл-таблицу
  
"""
def contact_update(service, driver):

    pay_curriencies = contact(driver)

    body = {
        "values": [
            [pay_curriencies["AZ_AZN"]],
            [pay_curriencies["AZ_USD"]],
            [pay_curriencies["GE_GEL"]],
            [pay_curriencies["GE_USD"]],
            [pay_curriencies["TJ_USD"]],
            [pay_curriencies["TR_USD"]],
            [pay_curriencies["UZ_USD"]],
            [pay_curriencies["KZ_USD"]],
            [pay_curriencies["KZ_KZT"]],
            [pay_curriencies["KG_USD"]],
        ]
    }

    SAMPLE_RANGE_NAME = "Котировки!G3"

    service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()

"""
    Функция импорта данных, полчуенных парсингом платежной системы CoronaPay в гугл-таблицу
  
"""
def coronapay_update(service):
    pay_curriencies = coronapay()

    body = {
        "values": [
            [pay_curriencies["UZB_RUS_1"]],
            [pay_curriencies["UZB_USD_2"]],
            [pay_curriencies["KAZ_KZT_3"]],
            [pay_curriencies["KAZ_USD_4"]],
            [pay_curriencies["CHN_USD_5"]],
            [pay_curriencies["TJK_USD_6"]],
            [pay_curriencies["KGZ_USD_7"]],
            [pay_curriencies["AZE_AZN_8"]],
            [pay_curriencies["AZE_USD_9"]],
            [pay_curriencies["TUR_TRY_10"]],
            [pay_curriencies["TUR_USD_11"]],
            [pay_curriencies["MDA_MDL_12"]],
            [pay_curriencies["MDA_USD_13"]],
            [pay_curriencies["GEO_GEL_14"]],
            [pay_curriencies["GEO_USD_15"]],
            [],
            [pay_curriencies["VNM_USD_17"]],
        ]
    }

    SAMPLE_RANGE_NAME = "Котировки!C3"

    service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()


"""
    Функция импорта данных, полчуенных парсингом платежной системы PaySend в гугл-таблицу
  
"""
def paysend_upadte(service):

    pay_curriencies = paysend()

    body = {"values": [[pay_curriencies["UZS_KGS_1"]], [pay_curriencies["KZT_KGS_2"]]]}

    SAMPLE_RANGE_NAME = "Котировки!O3"

    service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()


"""
    Функция импорта данных, полчуенных парсингом  криптобиржы OKX в гугл-таблицу
  
"""
def okx_p2p_update(service):
    pay_curriencies = okx_p2p()

    body = {
        "values": [
            [
                pay_curriencies["RussianStandardBank_buy_USDT_T"],
                pay_curriencies["RussianStandardBank_sell_USDT_T"],
                pay_curriencies["RaiffeisenBankAval_buy_USDT_T"],
                pay_curriencies["RaiffeisenBankAval_sell_USDT_T"],
                pay_curriencies["RaiffeisenBank_buy_USDT_T"],
                pay_curriencies["RaiffeisenBank_sell_USDT_T"],
                pay_curriencies["QIWI_buy_USDT_T"],
                pay_curriencies["QIWI_sell_USDT_T"],
                pay_curriencies["YandexMoneyNew_buy_USDT_T"],
                pay_curriencies["YandexMoneyNew_sell_USDT_T"],
            ],
            [
                pay_curriencies["RussianStandardBank_buy_BTC_T"],
                pay_curriencies["RussianStandardBank_sell_BTC_T"],
                pay_curriencies["RaiffeisenBankAval_buy_BTC_T"],
                pay_curriencies["RaiffeisenBankAval_sell_BTC_T"],
                pay_curriencies["RaiffeisenBank_buy_BTC_T"],
                pay_curriencies["RaiffeisenBank_sell_BTC_T"],
                pay_curriencies["QIWI_buy_BTC_T"],
                pay_curriencies["QIWI_sell_BTC_T"],
                pay_curriencies["YandexMoneyNew_buy_BTC_T"],
                pay_curriencies["YandexMoneyNew_sell_BTC_T"],
            ],
            [
                pay_curriencies["RussianStandardBank_buy_ETH_T"],
                pay_curriencies["RussianStandardBank_sell_ETH_T"],
                pay_curriencies["RaiffeisenBankAval_buy_ETH_T"],
                pay_curriencies["RaiffeisenBankAval_sell_ETH_T"],
                pay_curriencies["RaiffeisenBank_buy_ETH_T"],
                pay_curriencies["RaiffeisenBank_sell_ETH_T"],
                pay_curriencies["QIWI_buy_ETH_T"],
                pay_curriencies["QIWI_sell_ETH_T"],
                pay_curriencies["YandexMoneyNew_buy_ETH_T"],
                pay_curriencies["YandexMoneyNew_sell_ETH_T"],
            ],
        ]
    }

    SAMPLE_RANGE_NAME = "Котировки!B46"

    service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()


"""
    Функция импорта данных, полчуенных парсингом  криптобиржы ByBit в гугл-таблицу
  
"""
def bybit_p2p_update(service):
    pay_curriencies = bybit_p2p()

    body = {
        "values": [
            [
                pay_curriencies["RussianStandardBank_buy_USDT_T"],
                pay_curriencies["RussianStandardBank_sell_USDT_T"],
                pay_curriencies["RaiffeisenBankAval_buy_USDT_T"],
                pay_curriencies["RaiffeisenBankAval_sell_USDT_T"],
                # 0,
                # 0,
                # 0,
                # 0,
                pay_curriencies["RaiffeisenBank_buy_USDT_T"],
                pay_curriencies["RaiffeisenBank_sell_USDT_T"],
                pay_curriencies["QIWI_buy_USDT_T"],
                pay_curriencies["QIWI_sell_USDT_T"],
                pay_curriencies["YandexMoneyNew_buy_USDT_T"],
                pay_curriencies["YandexMoneyNew_sell_USDT_T"],
            ],
            [
                pay_curriencies["RussianStandardBank_buy_BTC_T"],
                pay_curriencies["RussianStandardBank_sell_BTC_T"],
                pay_curriencies["RaiffeisenBankAval_buy_BTC_T"],
                pay_curriencies["RaiffeisenBankAval_sell_BTC_T"],
                # 0,
                # 0,
                # 0,
                # 0,
                pay_curriencies["RaiffeisenBank_buy_BTC_T"],
                pay_curriencies["RaiffeisenBank_sell_BTC_T"],
                pay_curriencies["QIWI_buy_BTC_T"],
                pay_curriencies["QIWI_sell_BTC_T"],
                pay_curriencies["YandexMoneyNew_buy_BTC_T"],
                pay_curriencies["YandexMoneyNew_sell_BTC_T"],
            ],
            [
                pay_curriencies["RussianStandardBank_buy_ETH_T"],
                pay_curriencies["RussianStandardBank_sell_ETH_T"],
                pay_curriencies["RaiffeisenBankAval_buy_ETH_T"],
                pay_curriencies["RaiffeisenBankAval_sell_ETH_T"],
                # 0,
                # 0,
                # 0,
                # 0,
                pay_curriencies["RaiffeisenBank_buy_ETH_T"],
                pay_curriencies["RaiffeisenBank_sell_ETH_T"],
                pay_curriencies["QIWI_buy_ETH_T"],
                pay_curriencies["QIWI_sell_ETH_T"],
                pay_curriencies["YandexMoneyNew_buy_ETH_T"],
                pay_curriencies["YandexMoneyNew_sell_ETH_T"],
            ],
        ]
    }

    SAMPLE_RANGE_NAME = "Котировки!B37"

    service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()



"""
    Функция импорта данных, полчуенных парсингом спотовых котировок криптобиржы Binance в гугл-таблицу
  
"""
def binance_spot_update(service):
    pay_curriencies = binance_spot()

    body = {
        "values": [
            [
                pay_curriencies["USDT_RUB_1"],
                pay_curriencies["BNB_RUB_1"],
                pay_curriencies["BTC_RUB_1"],
                pay_curriencies["ETH_RUB_1"],
                pay_curriencies["SOL_RUB_1"],
                pay_curriencies["BUSD_RUB_1"],
                pay_curriencies["USDT_BTC_1"],
                pay_curriencies["USDT_ETH_1"],
                pay_curriencies["USDT_BNB_1"],
                pay_curriencies["USDT_BUSD_1"],
            ],
        ]
    }

    SAMPLE_RANGE_NAME = "Котировки!B33"

    service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()


"""
    Функция импорта данных, полчуенных парсингом  криптобиржы Binance в гугл-таблицу
  
"""
def binance_p2p_update(service):
    pay_curriencies = binance_p2p()

    body = {
        "values": [
            [
                pay_curriencies["RussianStandardBank_buy_USDT_T"],
                pay_curriencies["RussianStandardBank_sell_USDT_T"],
                # pay_curriencies['RaiffeisenBankAval_buy_USDT_T'],
                # pay_curriencies['RaiffeisenBankAval_sell_USDT_T'],
                0,
                0,
                # 0,
                # 0,
                pay_curriencies["RaiffeisenBank_buy_USDT_T"],
                pay_curriencies["RaiffeisenBank_sell_USDT_T"],
                pay_curriencies["QIWI_buy_USDT_T"],
                pay_curriencies["QIWI_sell_USDT_T"],
                pay_curriencies["YandexMoneyNew_buy_USDT_T"],
                pay_curriencies["YandexMoneyNew_sell_USDT_T"],
            ],
            [
                pay_curriencies["RussianStandardBank_buy_BTC_T"],
                pay_curriencies["RussianStandardBank_sell_BTC_T"],
                # pay_curriencies['RaiffeisenBankAval_buy_BTC_T'],
                # pay_curriencies['RaiffeisenBankAval_sell_BTC_T'],
                0,
                0,
                # 0,
                # 0,
                pay_curriencies["RaiffeisenBank_buy_BTC_T"],
                pay_curriencies["RaiffeisenBank_sell_BTC_T"],
                pay_curriencies["QIWI_buy_BTC_T"],
                pay_curriencies["QIWI_sell_BTC_T"],
                pay_curriencies["YandexMoneyNew_buy_BTC_T"],
                pay_curriencies["YandexMoneyNew_sell_BTC_T"],
            ],
            [
                pay_curriencies["RussianStandardBank_buy_ETH_T"],
                pay_curriencies["RussianStandardBank_sell_ETH_T"],
                # pay_curriencies['RaiffeisenBankAval_buy_ETH_T'],
                # pay_curriencies['RaiffeisenBankAval_sell_ETH_T'],
                0,
                0,
                # 0,
                # 0,
                pay_curriencies["RaiffeisenBank_buy_ETH_T"],
                pay_curriencies["RaiffeisenBank_sell_ETH_T"],
                pay_curriencies["QIWI_buy_ETH_T"],
                pay_curriencies["QIWI_sell_ETH_T"],
                pay_curriencies["YandexMoneyNew_buy_ETH_T"],
                pay_curriencies["YandexMoneyNew_sell_ETH_T"],
            ],
            [
                pay_curriencies["RussianStandardBank_buy_BNB_T"],
                pay_curriencies["RussianStandardBank_sell_BNB_T"],
                # pay_curriencies['RaiffeisenBankAval_buy_BNB_T'],
                # pay_curriencies['RaiffeisenBankAval_sell_BNB_T'],
                0,
                0,
                # 0,
                # 0,
                pay_curriencies["RaiffeisenBank_buy_BNB_T"],
                pay_curriencies["RaiffeisenBank_sell_BNB_T"],
                pay_curriencies["QIWI_buy_BNB_T"],
                pay_curriencies["QIWI_sell_BNB_T"],
                pay_curriencies["YandexMoneyNew_buy_BNB_T"],
                pay_curriencies["YandexMoneyNew_sell_BNB_T"],
            ],
            [
                pay_curriencies["RussianStandardBank_buy_RUB_T"],
                pay_curriencies["RussianStandardBank_sell_RUB_T"],
                # pay_curriencies['RaiffeisenBankAval_buy_RUB_T'],
                # pay_curriencies['RaiffeisenBankAval_sell_RUB_T'],
                0,
                0,
                # 0,
                # 0,
                pay_curriencies["RaiffeisenBank_buy_RUB_T"],
                pay_curriencies["RaiffeisenBank_sell_RUB_T"],
                pay_curriencies["QIWI_buy_RUB_T"],
                pay_curriencies["QIWI_sell_RUB_T"],
                pay_curriencies["YandexMoneyNew_buy_RUB_T"],
                pay_curriencies["YandexMoneyNew_sell_RUB_T"],
            ],
            [
                pay_curriencies["RussianStandardBank_buy_BUSD_T"],
                pay_curriencies["RussianStandardBank_sell_BUSD_T"],
                # pay_curriencies['RaiffeisenBankAval_buy_BUSD_T'],
                # pay_curriencies['RaiffeisenBankAval_sell_BUSD_T'],
                0,
                0,
                # 0,
                # 0,
                pay_curriencies["RaiffeisenBank_buy_BUSD_T"],
                pay_curriencies["RaiffeisenBank_sell_BUSD_T"],
                pay_curriencies["QIWI_buy_BUSD_T"],
                pay_curriencies["QIWI_sell_BUSD_T"],
                pay_curriencies["YandexMoneyNew_buy_BUSD_T"],
                pay_curriencies["YandexMoneyNew_sell_BUSD_T"],
            ],
        ]
    }

    SAMPLE_RANGE_NAME = "Котировки!B25"

    service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()



"""
    Функция импорта данных, полчуенных парсингом  криптобиржы Binance c фиатом UZS в гугл-таблицу
  
"""
def binance_p2p_uzs_update(service):
    pay_curriencies = binance_p2p_uzs()

    body = {
        "values": [
            [
                pay_curriencies["Humo_buy_USDT_T"],
                pay_curriencies["Humo_sell_USDT_T"],
                pay_curriencies["Uzcard_buy_USDT_T"],
                pay_curriencies["Uzcard_sell_USDT_T"],
                pay_curriencies["Kapitalbank_buy_USDT_T"],
                pay_curriencies["Kapitalbank_sell_USDT_T"],
                pay_curriencies["UzbekNationalBank_buy_USDT_T"],
                pay_curriencies["UzbekNationalBank_sell_USDT_T"],
            ]
        ]
    }

    SAMPLE_RANGE_NAME = "Котировки!C59"

    service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()

"""
    Функция импорта данных, полчуенных парсингом  криптобиржы Binance c фиатом KGS в гугл-таблицу
  
"""
def binance_p2p_kgs_update(service):
    pay_curriencies = binance_p2p_kgs()

    body = {
        "values": [
            [
                pay_curriencies["mBank_buy_USDT_T"],
                pay_curriencies["mBank_sell_USDT_T"],
                pay_curriencies["OPTIMABANK_buy_USDT_T"],
                pay_curriencies["OPTIMABANK_sell_USDT_T"],
                pay_curriencies["ELCART_buy_USDT_T"],
                pay_curriencies["ELCART_sell_USDT_T"],
                pay_curriencies["DEMIRBANK_buy_USDT_T"],
                pay_curriencies["DEMIRBANK_sell_USDT_T"],
            ]
        ]
    }

    SAMPLE_RANGE_NAME = "Котировки!C64"

    service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()


"""
    Функция импорта данных, полчуенных парсингом  криптобиржы Binance c фиатом KZT в гугл-таблицу
  
"""
def binance_p2p_kzt_update(service):
    pay_curriencies = binance_p2p_kzt()

    body = {
        "values": [
            [
                pay_curriencies["KaspiBank_buy_USDT_T"],
                pay_curriencies["KaspiBank_sell_USDT_T"],
                pay_curriencies["AltynBank_buy_USDT_T"],
                pay_curriencies["AltynBank_sell_USDT_T"],
                pay_curriencies["BankRBK_buy_USDT_T"],
                pay_curriencies["BankRBK_sell_USDT_T"],
                pay_curriencies["EurasianBank_buy_USDT_T"],
                pay_curriencies["EurasianBank_sell_USDT_T"],
            ]
        ]
    }

    SAMPLE_RANGE_NAME = "Котировки!C69"

    service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()


"""
    Функция импорта данных, полчуенных парсингом  криптобиржы Binance c фиатом TRY в гугл-таблицу
  
"""
def binance_p2p_try_update(service):
    pay_curriencies = binance_p2p_try()

    body = {
        "values": [
            [
                pay_curriencies["VakifBank_buy_USDT_T"],
                pay_curriencies["VakifBank_sell_USDT_T"],
                pay_curriencies["ISBANK_buy_USDT_T"],
                pay_curriencies["ISBANK_sell_USDT_T"],
                pay_curriencies["QNB_buy_USDT_T"],
                pay_curriencies["QNB_sell_USDT_T"],
                pay_curriencies["Ziraat_buy_USDT_T"],
                pay_curriencies["Ziraat_sell_USDT_T"],
            ]
        ]
    }

    SAMPLE_RANGE_NAME = "Котировки!C74"

    service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()



"""
    Функция импорта данных, полчуенных парсингом  криптобиржы Binance c фиатом GEL в гугл-таблицу
  
"""
def binance_p2p_gel_update(service):
    pay_curriencies = binance_p2p_gel()

    body = {
        "values": [
            [
                pay_curriencies["bank1_buy_USDT_T"],
                pay_curriencies["bank1_sell_USDT_T"],
                pay_curriencies["bank2_buy_USDT_T"],
                pay_curriencies["bank2_sell_USDT_T"],
                pay_curriencies["bank3_buy_USDT_T"],
                pay_curriencies["bank3_sell_USDT_T"],
                pay_curriencies["bank4_buy_USDT_T"],
                pay_curriencies["bank4_sell_USDT_T"],
            ]
        ]
    }

    SAMPLE_RANGE_NAME = "Котировки!C79"

    service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()



"""
    Функция импорта данных, полчуенных парсингом  криптобиржы Binance c фиатом TJS в гугл-таблицу
  
"""
def binance_p2p_tjs_update(service):
    pay_curriencies = binance_p2p_tjs()

    body = {
        "values": [
            [
                pay_curriencies["bank1_buy_USDT_T"],
                pay_curriencies["bank1_sell_USDT_T"],
                pay_curriencies["bank2_buy_USDT_T"],
                pay_curriencies["bank2_sell_USDT_T"],
                pay_curriencies["bank3_buy_USDT_T"],
                pay_curriencies["bank3_sell_USDT_T"],
                pay_curriencies["bank4_buy_USDT_T"],
                pay_curriencies["bank4_sell_USDT_T"],
            ]
        ]
    }

    SAMPLE_RANGE_NAME = "Котировки!C84"

    service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()


"""
    Функция импорта данных, полчуенных парсингом  криптобиржы Binance c фиатом AMD в гугл-таблицу
  
"""
def binance_p2p_amd_update(service):
    pay_curriencies = binance_p2p_amd()

    body = {
        "values": [
            [
                pay_curriencies["bank1_buy_USDT_T"],
                pay_curriencies["bank1_sell_USDT_T"],
                pay_curriencies["bank2_buy_USDT_T"],
                pay_curriencies["bank2_sell_USDT_T"],
                pay_curriencies["bank3_buy_USDT_T"],
                pay_curriencies["bank3_sell_USDT_T"],
                pay_curriencies["bank4_buy_USDT_T"],
                pay_curriencies["bank4_sell_USDT_T"],
            ]
        ]
    }

    SAMPLE_RANGE_NAME = "Котировки!C89"

    service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()


"""
    Функция импорта данных, полчуенных парсингом  криптобиржы Binance c фиатом AZN в гугл-таблицу
  
"""
def binance_p2p_azn_update(service):
    pay_curriencies = binance_p2p_azn()

    body = {
        "values": [
            [
                pay_curriencies["bank1_buy_USDT_T"],
                pay_curriencies["bank1_sell_USDT_T"],
                pay_curriencies["bank2_buy_USDT_T"],
                pay_curriencies["bank2_sell_USDT_T"],
                pay_curriencies["bank3_buy_USDT_T"],
                pay_curriencies["bank3_sell_USDT_T"],
                pay_curriencies["bank4_buy_USDT_T"],
                pay_curriencies["bank4_sell_USDT_T"],
            ]
        ]
    }

    SAMPLE_RANGE_NAME = "Котировки!M59"

    service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()


"""
    Функция импорта данных, полчуенных парсингом  криптобиржы Binance c фиатом MDL в гугл-таблицу
  
"""
def binance_p2p_mdl_update(service):
    pay_curriencies = binance_p2p_mdl()

    body = {
        "values": [
            [
                pay_curriencies["bank1_buy_USDT_T"],
                pay_curriencies["bank1_sell_USDT_T"],
                pay_curriencies["bank2_buy_USDT_T"],
                pay_curriencies["bank2_sell_USDT_T"],
                pay_curriencies["bank3_buy_USDT_T"],
                pay_curriencies["bank3_sell_USDT_T"],
            ]
        ]
    }

    SAMPLE_RANGE_NAME = "Котировки!M64"

    service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()


"""
    Функция обновления времени последнего парсинга в гугл-таблице
  
"""
def update_time(service):
    current_date = datetime.now(pytz.timezone("Europe/Moscow")).date()
    current_time = datetime.now(pytz.timezone("Europe/Moscow")).time()

    body = {"values": [[str(current_time).split(".", -1)[0] + " " + str(current_date)]]}

    SAMPLE_RANGE_NAME = "Международка!A6"

    service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()



config                = json_load(r'./json/config.json')
SAMPLE_SPREADSHEET_ID = config['SAMPLE_SPREADSHEET_ID']
CREDENTIALS_FILE      = "creds.json"

creds = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE, ["https://www.googleapis.com/auth/spreadsheets"]
)
httpAuth = creds.authorize(httplib2.Http())
service  = apiclient.discovery.build("sheets", "v4", http=httpAuth)

options = uc.ChromeOptions()
options.headless = True
options.add_argument("--headless")


browser = uc.Chrome(driver_executable_path=r'.\chromedriver.exe', options=options)

iter_count = 0

while True:
    if iter_count % 10 == 0:
        try:
            mirpay_update(service)
        except:
            pass

        try:
            unistream_update(service)
        except:
            pass

        try:
            contact_update(service, browser)
        except:
            pass

        try:
            coronapay_update(service)
        except:
            pass

        try:
            paysend_upadte(service)
        except:
            pass

    try:
        beribit_udpate(service)
    except:
        pass

    try:
        garantex_spot_update(service)
    except:
        pass

    try:
        okx_p2p_update(service)
    except:
        pass

    try:
        bybit_p2p_update(service)
    except:
        pass

    try:
        binance_spot_update(service)
    except:
        pass

    try:
        binance_p2p_update(service)
    except:
        pass

    try:
        binance_p2p_uzs_update(service)
    except:
        pass

    try:
        binance_p2p_kgs_update(service)
    except:
        pass

    try:
        binance_p2p_kzt_update(service)
    except:
        pass

    try:
        binance_p2p_try_update(service)
    except:
        pass

    try:
        binance_p2p_gel_update(service)
    except:
        pass

    try:
        binance_p2p_tjs_update(service)
    except:
        pass

    try:
        binance_p2p_amd_update(service)
    except:
        pass

    try:
        binance_p2p_azn_update(service)
    except:
        pass

    try:
        binance_p2p_mdl_update(service)
    except:
        pass

    update_time(service)
    iter_count += 1
