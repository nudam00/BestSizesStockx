import datetime
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def captcha():
    print("{}: Solve captcha".format(datetime.datetime.now()))
    time.sleep(5)


class Stockx:

    def __init__(self, driver, sku, email, password, price, rate_gbp, date, last_month, current_month):
        self.driver = driver
        self.sku = sku
        self.email = email
        self.password = password
        self.value = price
        self.rate_gbp = rate_gbp
        self.date = date
        self.last_month = last_month
        self.current_month = current_month

    def region(self):
        # Chooses region
        self.driver.get("https://stockx.com/")
        time.sleep(5)

        while True:
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@role="dialog"]/footer/button')))
                self.driver.find_element(
                    "xpath", '/html/body/div[6]/div[4]/div/section/footer/button').click()
                break
            except Exception:
                try:
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@role="dialog"]/footer/button')))
                    self.driver.find_element(
                        "xpath", '/html/body/div[5]/div[4]/div/section/footer/button').click()
                    break
                except Exception:
                    captcha()
                captcha()
        time.sleep(4)
        self.logging_in()

    def logging_in(self):
        # Logs in

        while True:
            try:
                self.driver.find_element(
                    'xpath', '//*[@id="nav-login"]').click()
                break
            except Exception:
                captcha()
        self.driver.refresh()

        while True:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="email-login"]')))
                self.driver.find_element(
                    'xpath', '//*[@id="email-login"]').send_keys(self.email)
                time.sleep(0.5)
                self.driver.find_element(
                    'xpath', '//*[@id="password-login"]').send_keys(self.password)
                time.sleep(2)
                break
            except Exception:
                captcha()

    def product_link(self):
        # Finds product link
        while True:
            try:
                self.driver.get(
                    "https://stockx.com/search/sneakers?s={}".format(self.sku))
                break
            except Exception:
                continue

        while True:
            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@data-testid="search-confirmation"]')))
                href = self.driver.find_element(
                    'xpath', '//*[@class="css-1dh562i"]')
                return href.find_element('css selector', 'a').get_attribute('href')
            except Exception:
                captcha()

    def priceRounding(self, price):
        if price % 10 > 5:
            return round(price, -1) - 10
        else:
            return round(price, -1)

    def item_info(self):
        # Gets product name, sku and sizes

        self.driver.get(self.product_link())

        # Scraps item names
        sizes = ""
        item_name = self.driver.find_element(
            'xpath', '//*[@class="chakra-heading css-1vj6v5q"]').get_attribute("innerText")

        # Scraps prices
        for s in range(1, 27):
            time.sleep(0.5)
            try:
                # Expands the size list
                while True:
                    try:
                        self.driver.find_element(
                            'xpath', '/html/body/div[1]/div/main/div/section[1]/div[3]/div[2]/div[2]/div[1]/div/button').click()
                        break
                    except Exception:
                        try:
                            self.driver.find_element(
                                'xpath', '/html/body/div[1]/div/main/div/section[1]/div[3]/div[2]/div[2]/div[1]/div/button').click()
                            break
                        except Exception:
                            try:
                                self.driver.find_element(
                                    'xpath', '/html/body/div[1]/div/main/div/section[1]/div[3]/div[2]/div[1]/div[1]/div/button').click()
                                break
                            except Exception:
                                print("Sth wrong")

                # Chooses appropriate size
                try:

                    self.driver.find_element(
                        'xpath', '//div[@class="css-1o6kz7w"]/button[{}]'.format(s)).click()

                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@class="css-3f2gt7"]/button[3]')))
                    self.driver.find_element(
                        'xpath', '//*[@class="css-3f2gt7"]/button[3]').click()

                    staleElement = True
                    date1 = 0
                    date_month = ""
                    count = 0
                    size = ""

                    # Checks last 20 purchases, saves last date
                    time.sleep(0.5)
                    while staleElement:
                        try:
                            count = len(self.driver.find_elements(
                                "class name", 'css-153ufkt'))
                            size = str(self.driver.find_element(
                                'xpath', '//tbody[@class="css-aydg0x"]/tr[1]/td[3]/p').get_attribute("innerText"))
                            date = str(self.driver.find_element(
                                'xpath', '//tbody[@class="css-aydg0x"]/tr[20]/td[1]/p').get_attribute('innerText'))
                            date_month = date[0:3]
                            date = date[4:6]
                            if ',' in date:
                                date = date.replace(',', '')
                            date1 = int(date)
                            staleElement = False
                        except Exception:
                            staleElement = True
                            if (count < 20) and (count != 0):
                                staleElement = False

                    # Closes last sales
                    while True:
                        try:
                            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                                (By.XPATH, '//*[@class="chakra-modal__close-btn css-1iqbypn"]')))
                            self.driver.find_element(
                                'xpath', '//*[@class="chakra-modal__close-btn css-1iqbypn"]').click()
                            break
                        except Exception:
                            self.driver.refresh()
                            break

                    # Highest bid
                    try:
                        price = int(self.driver.find_element('xpath', '//div[2]/a/p[@class="chakra-text css-itspem"]').get_attribute(
                            "innerText").replace('Sell for £', '').replace(' or Ask for More', ''))
                        price1 = (price - (price * 0.03) -
                                  (price * 0.07)) * self.rate_gbp
                        price1 = self.priceRounding(price1)
                        percent = (price1 - self.value) / self.value
                    except Exception:
                        price = int(self.driver.find_element(
                            'xpath', '//div[2]/div[1]/div[2]/div[2]/div/dl/dd[@class="chakra-stat__number css-1brf3jx"]').get_attribute("innerText").replace('£', ''))
                        price1 = (price - (price * 0.03) -
                                  (price * 0.07)) * self.rate_gbp
                        price1 = self.priceRounding(price1)
                        percent = (price1 - self.value) / self.value

                    # If margin is >= 15% then write size
                    if percent >= 0.15:
                        sizes += (size + ", ")
                        continue

                    # Lowest ask
                    try:
                        price = int(
                            self.driver.find_element('xpath', '//div[2]/div/a[2]/p[@class="chakra-text css-qhbnuv"]').get_attribute("innerText").replace('Buy for £', ''))
                        price1 = (price - (price * 0.03) -
                                  (price * 0.07)) * self.rate_gbp
                        price1 = self.priceRounding(price1)
                        percent = (price1 - self.value) / self.value
                    except Exception:
                        price = int(self.driver.find_element(
                            'xpath', '//div[2]/div[1]/div[2]/div[1]/div/dl/dd[@class="chakra-stat__number css-1brf3jx"]').get_attribute("innerText").replace('£', ''))
                        price1 = (price - (price * 0.03) -
                                  (price * 0.07)) * self.rate_gbp
                        price1 = self.priceRounding(price1)
                        percent = (price1 - self.value) / self.value

                    # If less than 20 sales, then pass
                    if (count < 20) and (count != 0):
                        continue

                    if self.date > 20:
                        if date_month != self.current_month or self.date - date1 > 20:
                            continue
                    elif self.date < 21:
                        if date_month != self.current_month and date_month != self.last_month:
                            continue
                        elif (self.date + 30) - date1 > 20 and date_month == self.last_month:
                            continue

                    # If margin is >= 15% then write size
                    if percent >= 0.15:
                        sizes += (size + ", ")
                        continue

                except Exception as e:
                    print(e)
                    continue
            except Exception as e:
                print(e)
                print('{}:Nothing for sale'.format(datetime.datetime.now()))

        return [item_name, sizes[:-2]]
