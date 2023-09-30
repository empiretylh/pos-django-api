from datetime import datetime
from django.test import TestCase
from .models import Sales as Sale
from .apiview import monthGenerator, yearGenerator

class YearGeneratorTestCase(TestCase):
    def setUp(self):
        # Create some test data for the year
        self.sales = [
            Sale(date=datetime(2022, 1, 1), grandtotal=100, tax=10),
            Sale(date=datetime(2022, 2, 1), grandtotal=200, tax=20),
            Sale(date=datetime(2022, 3, 1), grandtotal=0, tax=0),  # Add a month with no sales
            Sale(date=datetime(2022, 4, 1), grandtotal=400, tax=40),
            Sale(date=datetime(2022, 5, 1), grandtotal=500, tax=50),
            Sale(date=datetime(2022, 6, 1), grandtotal=600, tax=60),
            Sale(date=datetime(2022, 7, 1), grandtotal=700, tax=70),
            Sale(date=datetime(2022, 8, 1), grandtotal=800, tax=80),
            Sale(date=datetime(2022, 9, 1), grandtotal=900, tax=90),
            Sale(date=datetime(2022, 10, 1), grandtotal=1000, tax=100),
            Sale(date=datetime(2022, 11, 1), grandtotal=1100, tax=110),
            Sale(date=datetime(2022, 12, 1), grandtotal=1200, tax=120),
        ]

    def test_yearGenerator(self):
        # Call the yearGenerator function with the test data
        result = yearGenerator(self, self.sales)

        # Check that the result contains all 12 months
        self.assertEqual(len(result), 12)

        # Check that the result contains the correct total for each month
        self.assertEqual(result['Jan'], 90)
        self.assertEqual(result['Feb'], 180)
        self.assertEqual(result['Mar'], 0)  # Check that the result for March is 0
        self.assertEqual(result['Apr'], 360)
        self.assertEqual(result['May'], 450)
        self.assertEqual(result['Jun'], 540)
        self.assertEqual(result['Jul'], 630)
        self.assertEqual(result['Aug'], 720)
        self.assertEqual(result['Sep'], 810)
        self.assertEqual(result['Oct'], 900)
        self.assertEqual(result['Nov'], 990)
        self.assertEqual(result['Dec'], 1080)


from datetime import datetime
from django.test import TestCase
from .models import Expense
from .apiview import AyearGenerator

class AYearGeneratorTestCase(TestCase):
    def setUp(self):
        # Create some test data for the year
        self.expenses = [
            Expense(date=datetime(2022, 1, 1), price=100),
            Expense(date=datetime(2022, 2, 1), price=200),
            Expense(date=datetime(2022, 3, 1), price=300),
            Expense(date=datetime(2022, 4, 1), price=400),
            Expense(date=datetime(2022, 5, 1), price=500),
            Expense(date=datetime(2022, 6, 1), price=600),
            Expense(date=datetime(2022, 7, 1), price=700),
            Expense(date=datetime(2022, 8, 1), price=800),
            Expense(date=datetime(2022, 9, 1), price=900),
            Expense(date=datetime(2022, 10, 1), price=1000),
            Expense(date=datetime(2022, 11, 1), price=1100),
            Expense(date=datetime(2022, 12, 1), price=1200),
        ]

    def test_yearGenerator(self):
        # Call the yearGenerator function with the test data
        result = AyearGenerator(self, self.expenses)

        # Check that the result contains all 12 months
        self.assertEqual(len(result), 12)

        # Check that the result contains the correct total for each month
        self.assertEqual(result['Jan'], 100)
        self.assertEqual(result['Feb'], 200)
        self.assertEqual(result['Mar'], 300)
        self.assertEqual(result['Apr'], 400)
        self.assertEqual(result['May'], 500)
        self.assertEqual(result['Jun'], 600)
        self.assertEqual(result['Jul'], 700)
        self.assertEqual(result['Aug'], 800)
        self.assertEqual(result['Sep'], 900)
        self.assertEqual(result['Oct'], 1000)
        self.assertEqual(result['Nov'], 1100)
        self.assertEqual(result['Dec'], 1200)