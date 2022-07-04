# Best Sizes Checker
A program that writes the best sizes to an Excel file by comparing SKUs and prices from an Excel file to prices from StockX after commissions. Size is written out if the margin is more than 15% and if at least 20 units have been sold in the last 20 days.
Each first time the program is turned on at intervals, it ends up blocked by PerimeterX, in which case the program must be restarted and PerimeterX resolved. If there are no sales for a particular size, manually select the next size.
Written in Python using Selenium.

## stockx.py
A file that checks the price on StockX (modify StockX commision if you have different account level). It performs automatic logging, chooses region based on IP and compare all sizes to retail price.

## sizes.py
Returns all best sizes.

## main.py
It brings the whole program together. Calls classes based on data in shoes.xlsx and writes sizes to worth.xlsx.

## data.txt
Create file data.txt with:
1. Put Stockx email
2. Put Stockx password
3. Put GBP exchange rate with "." format
4. Put the day of the month
5. Put the name of the last month (first 3 letters, starting with a capital letter)
6. Put the name of the current month (first 3 letters, starting with a capital letter)

## shoes.xlsx
Write SKU and retail price in ZL (with "." format).

## worth.xslx
Look at best sizes.
