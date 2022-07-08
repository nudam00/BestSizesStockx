import os
from openpyxl import Workbook
from selenium import webdriver
import pandas as pd
from sizes import Sizes
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth


def openData():
    # Loads data from txt
    with open('data.txt', 'r') as file:
        txt = file.readlines()
    a = txt[0]
    b = txt[1]
    c = float(txt[2].replace("\n", ''))
    d = int(txt[3].replace("\n", ''))
    e = txt[4].replace("\n", '')
    f = txt[5].replace("\n", '')
    return [a, b, c, d, e, f]


def shoes(emai, passw, gbp, name, dat, driv, last_mont, current_mont):
    # Gets all needed data from sites
    df = pd.DataFrame(columns=['Product_name', 'SKU', 'Sizes', 'Quantity'])
    excel = pd.read_excel('shoes.xlsx', sheet_name=name)

    # Based on each row in excel sheet
    t = 0
    for index, row in excel.iterrows():
        sku = row['sku']
        value = row['price']

        sizes = Sizes(driv, sku, emai, passw, t, gbp,
                      value, dat, last_mont, current_mont)
        stockx = sizes.stockx()
        item_name = stockx[0]
        sizes = stockx[1]

        counter = sizes.count(",")
        counter += 1

        new_row = {'Product_name': item_name, 'SKU': sku,
                   'Sizes': sizes, 'Quantity': counter}
        df = df.append(new_row, ignore_index=True)
        print('\n' + item_name)
        print(sku)
        print(sizes)

        t += 1

    return df


def main():
    print('data.txt, in each row:\n'
          '1. Enter StockX email\n'
          '2. Enter StockX password\n'
          '3. Enter the GBP exchange rate in the format "."\n'
          '4. Enter the current date of the month\n'
          '5. Enter the name of the last month (first 3 letters, starting with a capital letter)\n'
          '6. Enter the name of the current month (first 3 letters, starting with a capital letter)\n'
          '\n'
          'shoes.xlsx, in each row:\n'
          '1. Write SKUs\n'
          '2. Write prices\n'
          '\n'
          'Write anything if you wish to start')
    input()

    try:
        os.remove("worth.xlsx")
    except FileNotFoundError:
        pass
    wb = Workbook()
    wb.save(filename='worth.xlsx')
    data = openData()
    email = data[0]
    password = data[1]
    kurs_gbp = data[2]
    date = data[3]
    last_month = data[4]
    current_month = data[5]
    sheets = pd.ExcelFile('shoes.xlsx').sheet_names

    options = Options()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    s = Service('C:\\BrowserDrivers\\chromedriver.exe')
    driver = webdriver.Chrome(options=options,
                              executable_path="C:/Users/dratw/Documents/PythonProjects/bestSizeChecker/chromedriver.exe")
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    # Based on each sheet in excel file
    for i in range(len(pd.ExcelFile('shoes.xlsx').sheet_names)):
        stock = shoes(email, password, kurs_gbp, i, date,
                      driver, last_month, current_month)
        with pd.ExcelWriter('worth.xlsx', engine='openpyxl', mode='a') as writer:
            stock.to_excel(writer, sheet_name=sheets[i])

    writer.save()
    writer.close()


if __name__ == "__main__":
    main()
