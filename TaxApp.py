from dataclasses import dataclass

@dataclass
class Product:
    """
    Product is a data class that contains information about one product
    and its quantity.
    """
    quantity: int       # number of items
    productName: str    # name of the product
    priceCent: int      # price in cent
    imported: bool      # was the product imported
    exempt: bool        # is it emempt from sales tax

@dataclass
class TaxConfig:
    """
    TaxConfigis a data class that contains information about parameters
    of the tax calculation.
    """
    salesTaxRate: int = 10 # in percent
    importDutyRate: int = 5 # in percent

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
        pass

    def generateReceipt(self):
        """
        generateReceipt uses all self.products to generate a receipt as a text

        :param line: A string to retrieve information from.
        :return: the receipt as a string
        """
        return ""

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
