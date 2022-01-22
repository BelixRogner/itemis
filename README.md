# itemis coding challenge

usage
-----
run TaxApp.py
enter one line/product at a time
press enter (don't give any input) to print the receipt


assumptions
-----
- each product has to have its own line fitting this regex (case insensitive): "^(\d+) (.*) at ([-+]?\d+)\.(\d{2})$"
- the input price is meant for the quantity of 1
- multiple whitespaces should be ignored in the product name
- an imported product has the substring "imported"
- if a product is imported it should be the first part of the product name
- round up to the nearest 0.05 means:
  round n up to the nearest 0.05, which is >= n
