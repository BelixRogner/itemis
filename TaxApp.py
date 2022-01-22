from dataclasses import dataclass
import re

CENT_PER_EURO: int = 100
@dataclass
class Product:
    """
    Product is a data class that contains information about one product
    and its quantity.
    """
    quantity: int       # number of items
    productName: str    # name of the product
    priceCent: int      # price in cent
    imported: bool      # was the product imported?
    exempt: bool        # is it exempt from sales tax?

@dataclass
class TaxConfig:
    """
    TaxConfigis a data class that contains information about parameters
    of the tax calculation.
    """
    salesTaxRate: int = 10 # in percent
    importDutyRate: int = 5 # in percent
    rateDenominator: int = 100 # divisor for the tax rates
    taxRound: int = 5 # round up to every _ cent

    # items which are exempt from sales tax
    exemptProducts = ("magazine", "book", "food", "pill", "vaccine", "drug",
                        "antibiotic", "chocolate", "milk")

class TaxApp:
    def __init__(self, taxConfig):
        """
        Constructor creates an empty list of products.

        :param taxConfig: An instance of class TaxConfig to set relevant
                        parameters for calculating the taxes.
        """
        self.conf = taxConfig
        self.products = list()


    def parseOneProduct(self, line):
        """
        parseOneProduct parses a string about one product, creates a
                        instance of the class Product and adds it to
                        self.products.

        :param line: A string to retrieve information from.
        """
        # delete whitespaces at start and end
        line = line.strip()
        # delete multiple whitespaces
        line = re.sub(' +', ' ', line)

        # 4 capturing groups:
        # 1. After start of string atleast one number
        # 2. any string
        # 3. optionlly + or - with one or more numbers
        # 4. 2 numbers
        p = re.compile("^(\d+) (.*) at ([-+]?\d+)\.(\d{2})$", re.IGNORECASE)
        m = p.match(line)
        if not m:
            raise ValueError("Invalid string")

        quantity = int(m.group(1))
        productName = m.group(2)
        priceEuro = int(m.group(3))
        priceCent = int(m.group(4))

        # product is imported if the product name contains the string
        # case insensitive
        imported = bool(re.search('imported', productName, re.IGNORECASE))

        if imported:
            # place "imported" to the beginning of the product name
            productName = re.sub('imported', '', productName, flags=re.IGNORECASE)
            productName = f"imported {productName}"

        # delete unnecessary whitespaces
        productName = re.sub(' +', ' ', productName)
        productName = productName.strip()

        # convert euros to cent and add to the sum
        priceCent += priceEuro * CENT_PER_EURO

        # add product to list
        self.products.append(
            Product(quantity,
                    productName,
                    priceCent,
                    imported,
                    self.isExempted(productName)))


    def generateReceipt(self):
        """
        generateReceipt uses all [self.products] to generate a receipt as a text

        :return: the receipt as a string
        """
        taxSum = 0      # sum of all taxes
        totalPrice = 0  # total price including tax
        receipt = ""

        for prod in self.products:
            # calculate total tax for this product
            tax = self.calculateTax(prod) * prod.quantity
            taxSum += tax

            grossPrice = prod.priceCent * prod.quantity + tax

            totalPrice += grossPrice

            receipt += f"{prod.quantity} {prod.productName}: {self.centsToStr(grossPrice)}\n"


        receipt += f"Sales Taxes: {self.centsToStr(taxSum)}\n"

        receipt += f"Total: {self.centsToStr(totalPrice)}\n"
        return receipt


    def isExempted(self, productName):
        """
        isExempted checks if a product is eligible for tax exemption

        :param productName: A string to retrieve information from.
        :return: is product exempted?
        """
        for prod in self.conf.exemptProducts:
            if prod in productName:
                return True
        return False


    def roundUp(self, num, divisor):
        """
        roundUp rounds [num] to the nearest number, that is divisible
                by [divisor] and larger or equal to num

        :param num: Number to round
        :param divisor: The number to round to
        :return: rounded number
        """
        quotient = num // divisor
        remainder = num % divisor
        # if the remainder is non zero, it will increase the quotient by one
        return (quotient + (remainder != 0)) * divisor


    def centsToStr(self, cents):
        """
        centsToStr formats an amount of cents to a string like "12.34"

        :param cents: amount of cents
        :return: formatted string
        """
        euros = cents // CENT_PER_EURO
        cents = cents % CENT_PER_EURO
        return f"{euros}.{cents:02d}"


    def calculateTax(self, prod):
        """
        calculateTax calculates the tax for one item of [prod]

        :param prod: product to calculate taxes for
        :return: tax for a quantity of 1 in cents
        """
        # get sales tax rate if required
        taxRate = 0 if prod.exempt else self.conf.salesTaxRate

        # add import tax if required
        if prod.imported:
            taxRate += self.conf.importDutyRate

        # calculate tax
        tax = taxRate * prod.priceCent

        # first round the number and then divide by rateDenominator to
        # prevent rounding inaccuracies
        # For example: taxRate = 5; priceCent = 110
        # tax = 5 * 110 = 550 (cent)
        # 550 // 100 = 5 which would be rounded to 5 (wrong)
        # To prevent that, it will be first rounded to the next 500
        # roundUp(550, 500) = 1000
        # 1000 // 100 = 10 (right)
        return self.roundUp(tax, self.conf.taxRound * self.conf.rateDenominator) // self.conf.rateDenominator


def main():
    conf = TaxConfig()
    app = TaxApp(conf)
    # take user input
    userInput = input()
    try:
        # parse user input until the input is empty
        while userInput:
            app.parseOneProduct(userInput)
            userInput = input()
    # if input is invalid
    except ValueError as e:
        print(f"Error: {e}")
        return
    print(app.generateReceipt())


if __name__ == "__main__":
    main()
