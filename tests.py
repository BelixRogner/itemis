import unittest
from TaxApp import TaxApp, TaxConfig

def getOutput(testNum, modified=False):
    """
    getOutput reads a test output file and returns the content.

    :param testNum: The number of the test.
    :param modified: Does it use a modified tax configuration?
    :return: Content of file as string
    """
    with open(f"tests/output{testNum}{'_m' if modified else ''}.txt", "r") as file:
        output = file.read()
    return output

class TestStandardConf(unittest.TestCase):
    def setUp(self):
        conf = TaxConfig()
        self.app = TaxApp(conf)

    def loadInput(self, testNum):
        """
        loadInput reads a test input file and parses each line using the TaxApp.

        :param testNum: The number of the test.
        """
        with open(f"tests/input{testNum}.txt", "r") as file:
            for line in file.readlines():
                self.app.parseOneProduct(line)

    def test_case0(self):
        i = 0
        self.loadInput(i)
        self.assertEqual(getOutput(i), self.app.generateReceipt())

    def test_case1(self):
        i = 1
        self.loadInput(i)
        self.assertEqual(getOutput(i), self.app.generateReceipt())

    def test_case2(self):
        i = 2
        self.loadInput(i)
        self.assertEqual(getOutput(i), self.app.generateReceipt())

    def test_case3(self):
        i = 3
        self.loadInput(i)
        self.assertEqual(getOutput(i), self.app.generateReceipt())

    def test_case4(self):
        i = 4
        self.loadInput(i)
        self.assertEqual(getOutput(i), self.app.generateReceipt())

    def test_case5(self):
        i = 5
        self.loadInput(i)
        self.assertEqual(getOutput(i), self.app.generateReceipt())


    def testInvalidInput(self):
        with self.assertRaises(ValueError):
            self.app.parseOneProduct("trash")

        with self.assertRaises(ValueError):
            self.app.parseOneProduct("")


class TestModifiedConf(unittest.TestCase):
    def setUp(self):
        conf = TaxConfig(salesTaxRate=20)
        self.app = TaxApp(conf)

    def loadInput(self, testNum):
        """
        loadInput reads a test input file and parses each line using the TaxApp.

        :param testNum: The number of the test.
        """
        with open(f"tests/input{testNum}.txt", "r") as file:
            for line in file.readlines():
                self.app.parseOneProduct(line)

    def test_case0(self):
        i = 0
        self.loadInput(i)
        self.assertEqual(getOutput(i, True), self.app.generateReceipt())

    def test_case1(self):
        i = 1
        self.loadInput(i)
        self.assertEqual(getOutput(i, True), self.app.generateReceipt())

if __name__ == '__main__':
    unittest.main()
